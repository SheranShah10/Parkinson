"""
Merge Validator Module
"""
import pandas as pd

class MergeValidator:
    def write_diagnostics(self, diagnostics: list, filepath: str):
        lines = ["# Merge Diagnostics\n"]
        lines.append("| Dataset | Strategy | Rows Before | Dropped | Master After |")
        lines.append("|---|---|---|---|---|")
        for d in diagnostics:
            lines.append(f"| {d['dataset']} | {d['strategy']} | {d['df_before']} | {d['dropped']} | {d['master_after']} |")
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
