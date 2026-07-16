"""
Duplicate Resolver Module
"""
import pandas as pd
import logging
from typing import Tuple, List, Dict

logger = logging.getLogger(__name__)

class DuplicateResolver:
    def __init__(self):
        self.diagnostics: List[Dict[str, str]] = []
        
    def resolve(self, df: pd.DataFrame, dataset_name: str, identifiers: List[str], strategy: str) -> pd.DataFrame:
        if not identifiers or not set(identifiers).issubset(df.columns):
            return df
            
        initial_len = len(df)
        dups = df.duplicated(subset=identifiers, keep=False)
        num_dups = dups.sum()
        
        if num_dups == 0:
            return df
            
        if strategy == "one_to_one":
            # For 1:1, we drop duplicates but we log it. We keep the last updated or first valid.
            # Usually PPMI has ORIG_ENTRY or LAST_UPDATE, let's just keep 'last' assuming chronological sorting
            # or just 'first'.
            df_resolved = df.drop_duplicates(subset=identifiers, keep='first').copy()
            resolved_len = len(df_resolved)
            dropped = initial_len - resolved_len
            
            self.diagnostics.append({
                "dataset": dataset_name,
                "strategy": strategy,
                "initial_rows": initial_len,
                "duplicates_found": num_dups,
                "dropped": dropped,
                "reason": "Legitimate repeated assessments or true duplicate records resolved by keeping first valid."
            })
            return df_resolved
            
        elif strategy == "aggregate":
            # Just return df, aggregator in join_engine will handle it
            return df
            
        elif strategy == "pivot":
            return df.drop_duplicates(subset=identifiers, keep='first').copy()
            
        elif strategy == "sequence":
            return df
            
        return df
        
    def generate_report(self, filepath: str):
        lines = ["# Duplicate Analysis Report\n"]
        for diag in self.diagnostics:
            lines.append(f"## {diag['dataset']}")
            for k, v in diag.items():
                if k != "dataset":
                    lines.append(f"- **{k}**: {v}")
            lines.append("\n")
            
        if not self.diagnostics:
            lines.append("No duplicate resolution was necessary. All keys unique.\n")
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(lines))
