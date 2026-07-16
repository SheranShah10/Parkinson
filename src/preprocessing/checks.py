"""
Checks Module

Responsibility: Post-alignment consistency checks.
"""
import pandas as pd
from typing import Dict, Any

class ConsistencyValidator:
    @staticmethod
    def validate(df: pd.DataFrame) -> Dict[str, Any]:
        report = {}
        
        if 'PATNO' in df.columns and 'EVENT_ID' in df.columns:
            dups = df.duplicated(subset=['PATNO', 'EVENT_ID']).sum()
            report["duplicate_visits"] = int(dups)
        else:
            report["duplicate_visits"] = -1
            
        # Check targets
        if 'TARGET_NHY' in df.columns:
            report["missing_nhy_targets"] = int(df['TARGET_NHY'].isna().sum())
            
        return report
