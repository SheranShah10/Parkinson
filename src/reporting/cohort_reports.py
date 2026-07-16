"""
Cohort Reports Module
"""
import os
import json
import pandas as pd
from typing import Dict, Any

class CohortReporter:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_markdown(self, checks: Dict[str, Any], flow: dict, df: pd.DataFrame):
        lines = ["# Cohort Construction Report\n"]
        lines.append("## Inclusion/Exclusion Flow")
        for k, v in flow.items():
            lines.append(f"- **{k}**: {v}")
            
        lines.append("\n## Consistency Checks")
        for k, v in checks.items():
            lines.append(f"- **{k}**: {v}")
            
        lines.append("\n## Target Generation Summary")
        if 'TARGET_NHY' in df.columns:
            lines.append(f"- Non-null NHY targets: {df['TARGET_NHY'].notna().sum()}")
        if 'TARGET_TOTAL_UPDRS' in df.columns:
            lines.append(f"- Non-null UPDRS targets: {df['TARGET_TOTAL_UPDRS'].notna().sum()}")
            
        with open(os.path.join(self.output_dir, 'cohort_report.md'), 'w') as f:
            f.write("\n".join(lines))
            
    def generate_json(self, checks: dict, flow: dict):
        stats = {"checks": checks, "flow": flow}
        with open(os.path.join(self.output_dir, 'cohort_statistics.json'), 'w') as f:
            json.dump(stats, f, indent=4)
