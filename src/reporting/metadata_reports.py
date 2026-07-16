"""
Metadata Reports Module
"""
import os
import json
import pandas as pd
from typing import List, Dict, Any

class MetadataReporter:
    def __init__(self, reports_dir: str, meta_dir: str):
        self.reports_dir = reports_dir
        self.meta_dir = meta_dir
        os.makedirs(reports_dir, exist_ok=True)
        os.makedirs(meta_dir, exist_ok=True)
        
    def write_inventories(self, datasets: List[Dict[str, Any]]):
        df = pd.DataFrame(datasets)
        # Drop complex types for CSV
        df_csv = df.drop(columns=['columns_list', 'dtypes'])
        
        df_csv.to_csv(os.path.join(self.reports_dir, 'dataset_inventory.csv'), index=False)
        df_csv.to_csv(os.path.join(self.reports_dir, 'metadata_dataset_registry.csv'), index=False)
        
        # Save JSON catalog
        df.to_json(os.path.join(self.meta_dir, 'dataset_catalog.json'), orient='records', indent=4)
        
    def write_schemas(self, schemas: Dict[str, Any]):
        with open(os.path.join(self.reports_dir, 'schema_registry.json'), 'w') as f:
            json.dump(schemas, f, indent=4)
        with open(os.path.join(self.meta_dir, 'column_catalog.json'), 'w') as f:
            json.dump(schemas, f, indent=4)
            
    def write_relationships(self, rels: Dict[str, Any], mermaid: str):
        with open(os.path.join(self.meta_dir, 'merge_catalog.json'), 'w') as f:
            json.dump(rels, f, indent=4)
            
        lines = ["# Dataset Relationships\n", "## ER Diagram\n", "```mermaid\n" + mermaid + "\n```"]
        with open(os.path.join(self.reports_dir, 'dataset_relationships.md'), 'w') as f:
            f.write("\n".join(lines))
            
    def write_data_dictionary(self, schemas: Dict[str, Any]):
        lines = ["# Data Dictionary\n"]
        for ds_name, sch in schemas.items():
            lines.append(f"## {ds_name}\n")
            lines.append("| Column | Type | Numeric | Description |")
            lines.append("|---|---|---|---|")
            for col, meta in sch.items():
                lines.append(f"| {col} | {meta['type']} | {meta['is_numeric']} | {meta['description']} |")
            lines.append("\n")
            
        with open(os.path.join(self.reports_dir, 'data_dictionary.md'), 'w') as f:
            f.write("\n".join(lines))
            
    def write_validation_report(self, errors: List[str]):
        lines = ["# Metadata Validation Report\n"]
        if not errors:
            lines.append("No metadata inconsistencies found! All datasets correctly conform to standard keys.")
        else:
            for e in errors:
                lines.append(f"- {e}")
                
        with open(os.path.join(self.reports_dir, 'metadata_validation_report.md'), 'w') as f:
            f.write("\n".join(lines))
            
    def write_modality_catalog(self, datasets: List[Dict[str, Any]]):
        modalities = {}
        for ds in datasets:
            mod = ds['modality']
            if mod not in modalities:
                modalities[mod] = []
            modalities[mod].append(ds['name'])
            
        with open(os.path.join(self.meta_dir, 'modality_catalog.json'), 'w') as f:
            json.dump(modalities, f, indent=4)
