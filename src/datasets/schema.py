"""
Schema Module

Responsibility: Infer schema, detect identifiers, detect column types.
"""
import pandas as pd
from typing import Dict, Any, List

class SchemaInferencer:
    IDENTIFIERS = ["PATNO", "EVENT_ID", "INFODT", "VISIT", "VISIT_ID", "PAG_NAME", "IMAGE_ID"]

    @staticmethod
    def infer(filepath: str) -> Dict[str, Any]:
        ext = filepath.split('.')[-1].lower()
        if ext not in ['csv', 'tsv', 'txt', 'xls', 'xlsx', 'parquet']:
            return {"status": "unsupported"}
            
        try:
            if ext in ['csv', 'tsv', 'txt']:
                sep = '\t' if ext in ['tsv', 'txt'] else ','
                df = pd.read_csv(filepath, sep=sep, low_memory=False, nrows=5000)
            elif ext in ['xls', 'xlsx']:
                df = pd.read_excel(filepath, nrows=5000)
            elif ext == 'parquet':
                df = pd.read_parquet(filepath)
        except:
            return {"status": "error_reading"}
            
        columns = list(df.columns)
        found_ids = [c for c in columns if c.upper() in SchemaInferencer.IDENTIFIERS]
        missing_ids = [i for i in SchemaInferencer.IDENTIFIERS if i not in [c.upper() for c in columns]]
        
        date_cols = [c for c in columns if 'date' in c.lower() or 'dt' in c.lower()]
        
        continuous = []
        categorical = []
        
        for c in columns:
            if c in found_ids or c in date_cols:
                continue
            if pd.api.types.is_numeric_dtype(df[c]):
                if df[c].nunique() < 20:
                    categorical.append(c)
                else:
                    continuous.append(c)
            else:
                categorical.append(c)
                
        return {
            "status": "success",
            "columns": columns,
            "found_identifiers": found_ids,
            "missing_identifiers": missing_ids,
            "date_columns": date_cols,
            "continuous_columns": continuous,
            "categorical_columns": categorical
        }
