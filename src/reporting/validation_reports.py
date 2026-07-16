"""
Validation Reports Module
"""
import os
import json
import pandas as pd
from typing import List, Dict, Any

class ValidationReporter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_registry(self, registry: List[Dict[str, Any]]):
        df = pd.DataFrame(registry)
        for col in df.columns:
            if df[col].apply(lambda x: isinstance(x, list)).any():
                df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
        df.to_csv(os.path.join(self.output_dir, "dataset_registry.csv"), index=False)

    def generate_schema_registry(self, schemas: Dict[str, Any]):
        with open(os.path.join(self.output_dir, "schema_registry.json"), 'w') as f:
            json.dump(schemas, f, indent=4)
            
    def generate_markdown_reports(self, logs: List[Dict[str, Any]], registry: List[Dict[str, Any]]):
        df = pd.DataFrame(registry)
        
        # Extraction report
        ext_lines = ["# ZIP Extraction Report\n"]
        for log in logs:
            ext_lines.append(f"- **{log['archive_name']}**: {log['status']} ({log.get('error_message', 'No errors')})")
        with open(os.path.join(self.output_dir, "zip_extraction_report.md"), 'w') as f:
            f.write("\n".join(ext_lines))
            
        # Validation report
        val_lines = ["# Validation Report\n"]
        val_lines.append(f"Total datasets scanned: {len(registry)}\n")
        val_lines.append(f"Valid datasets: {sum(1 for r in registry if r['is_valid'])}\n")
        with open(os.path.join(self.output_dir, "validation_report.md"), 'w') as f:
            f.write("\n".join(val_lines))
            
        # Corrupted / Unsupported
        corr_lines = ["# Corrupted Files Report\n"]
        unsup_lines = ["# Unsupported Files Report\n"]
        for r in registry:
            if not r['is_valid']:
                if "Unsupported" in str(r.get('validation_errors', '')):
                    unsup_lines.append(f"- **{r['dataset_name']}**: {r['validation_errors']}")
                else:
                    corr_lines.append(f"- **{r['dataset_name']}**: {r['validation_errors']}")
                    
        with open(os.path.join(self.output_dir, "corrupted_files_report.md"), 'w') as f:
            f.write("\n".join(corr_lines))
        with open(os.path.join(self.output_dir, "unsupported_files_report.md"), 'w') as f:
            f.write("\n".join(unsup_lines))
            
    def generate_all(self, logs: List[Dict[str, Any]], registry: List[Dict[str, Any]], schemas: Dict[str, Any]):
        self.generate_registry(registry)
        self.generate_schema_registry(schemas)
        self.generate_markdown_reports(logs, registry)
