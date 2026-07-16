"""
Inventory Reports Module

Responsibility: Generate publication-quality reports in CSV, JSON, and Markdown.
"""

import os
import json
import pandas as pd
from typing import List, Dict, Any

class InventoryReporter:
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_csv_json(self, inventory: List[Dict[str, Any]]):
        df = pd.DataFrame(inventory)
        # Handle non-serializable columns gracefully
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, (list, dict, set))).any():
                df[col] = df[col].apply(lambda x: json.dumps(list(x)) if isinstance(x, set) else json.dumps(x) if isinstance(x, (list, dict)) else x)
        
        df.to_csv(os.path.join(self.output_dir, "dataset_inventory.csv"), index=False)
        
        # Save raw JSON safely
        safe_inventory = json.loads(df.to_json(orient='records'))
        with open(os.path.join(self.output_dir, "dataset_summary.json"), 'w') as f:
            json.dump(safe_inventory, f, indent=4)
            
        return df

    def generate_catalog_md(self, df: pd.DataFrame):
        lines = ["# Dataset Catalog\n"]
        lines.append("A complete registry of all discovered datasets.\n")
        
        if df.empty:
            lines.append("No datasets found.")
        else:
            for cat, group in df.groupby("category"):
                lines.append(f"## {cat}")
                for _, row in group.iterrows():
                    lines.append(f"### {row['file_name']}")
                    lines.append(f"- **Path**: `{row['relative_path']}`")
                    lines.append(f"- **Size**: {row.get('file_size_bytes', 0) / (1024*1024):.2f} MB")
                    lines.append(f"- **Rows**: {row.get('num_rows', 'N/A')}")
                    lines.append(f"- **Columns**: {row.get('num_columns', 'N/A')}")
                    lines.append("")
                    
        with open(os.path.join(self.output_dir, "dataset_catalog.md"), 'w') as f:
            f.write("\n".join(lines))

    def generate_quality_md(self, df: pd.DataFrame):
        lines = ["# Data Quality Report\n"]
        
        if not df.empty and 'dataset_type' in df.columns:
            tabular = df[df['dataset_type'] == 'tabular']
            lines.append("## Missing Values (Top 10)")
            missing = tabular.nlargest(10, 'missing_percentage')
            for _, row in missing.iterrows():
                lines.append(f"- **{row['file_name']}**: {row.get('missing_percentage', 0):.2f}%")
                
            lines.append("\n## Duplicate Rows (Top 10)")
            dupes = tabular.nlargest(10, 'duplicate_rows')
            for _, row in dupes.iterrows():
                if row.get('duplicate_rows', 0) > 0:
                    lines.append(f"- **{row['file_name']}**: {row['duplicate_rows']} duplicates")
                    
        with open(os.path.join(self.output_dir, "dataset_quality_report.md"), 'w') as f:
            f.write("\n".join(lines))

    def generate_relationships_md(self, relationships: List[Dict[str, Any]]):
        lines = ["# Dataset Relationships Map\n"]
        if not relationships:
            lines.append("No common keys discovered.")
        else:
            for rel in relationships:
                lines.append(f"- **{rel['source']}** <--> **{rel['target']}** (Keys: `{', '.join(rel['keys'])}`)")
                
        with open(os.path.join(self.output_dir, "dataset_relationships.md"), 'w') as f:
            f.write("\n".join(lines))

    def generate_all(self, inventory: List[Dict[str, Any]], relationships: List[Dict[str, Any]]):
        df = self.generate_csv_json(inventory)
        self.generate_catalog_md(df)
        self.generate_quality_md(df)
        self.generate_relationships_md(relationships)
