"""
Schema Generator Module
"""
import pandas as pd
from typing import Dict, Any

class SchemaGenerator:
    def generate_schema(self, stats: Dict[str, Any]) -> Dict[str, Any]:
        schema = {}
        for col, dtype in stats.get("dtypes", {}).items():
            is_numeric = 'int' in dtype or 'float' in dtype
            meaning = self._infer_meaning(col)
            schema[col] = {
                "type": dtype,
                "is_numeric": is_numeric,
                "description": meaning
            }
        return schema
        
    def _infer_meaning(self, col: str) -> str:
        c = col.upper()
        if c == 'PATNO': return "Patient Identifier"
        if c == 'EVENT_ID': return "Visit Identifier"
        if c == 'INFODT': return "Information Date"
        if 'UPDRS' in c: return "MDS-UPDRS Clinical Score"
        if 'NHY' in c: return "Hoehn & Yahr Stage"
        if 'AGE' in c: return "Age of Participant"
        if c == 'SEX': return "Sex of Participant"
        return "Unknown/Standard feature"
