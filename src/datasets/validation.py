"""
Validation Module

Responsibility: Verify file integrity, encoding, formatting, and duplicates.
"""
import os
import pandas as pd
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DatasetValidator:
    SUPPORTED_EXTENSIONS = {'.csv', '.tsv', '.txt', '.xls', '.xlsx', '.parquet'}

    @staticmethod
    def validate(filepath: str) -> Dict[str, Any]:
        ext = os.path.splitext(filepath)[1].lower()
        result = {
            "is_valid": True,
            "is_supported": True,
            "is_empty": False,
            "has_duplicate_columns": False,
            "has_duplicate_rows": False,
            "error_message": None,
            "warnings": []
        }

        if ext not in DatasetValidator.SUPPORTED_EXTENSIONS:
            result["is_valid"] = False
            result["is_supported"] = False
            result["error_message"] = "Unsupported file format."
            return result

        if os.path.getsize(filepath) == 0:
            result["is_valid"] = False
            result["is_empty"] = True
            result["error_message"] = "File is empty."
            return result

        try:
            if ext in ['.csv', '.tsv', '.txt']:
                sep = '\t' if ext in ['.tsv', '.txt'] else ','
                # Read 500 rows for fast validation to avoid OOM on huge files
                df = pd.read_csv(filepath, sep=sep, low_memory=False, nrows=5000)
            elif ext in ['.xls', '.xlsx']:
                df = pd.read_excel(filepath, nrows=5000)
            elif ext == '.parquet':
                df = pd.read_parquet(filepath)
                
            if len(df.columns) != len(set(df.columns)):
                result["has_duplicate_columns"] = True
                result["warnings"].append("Duplicate column names detected.")
                
            dup_rows = df.duplicated().sum()
            if dup_rows > 0:
                result["has_duplicate_rows"] = True
                result["warnings"].append(f"{dup_rows} duplicate rows detected.")
                
        except UnicodeDecodeError:
            result["is_valid"] = False
            result["error_message"] = "Invalid encoding (not UTF-8)."
        except pd.errors.ParserError:
            result["is_valid"] = False
            result["error_message"] = "Invalid delimiters or corrupted formatting."
        except Exception as e:
            result["is_valid"] = False
            result["error_message"] = str(e)
            
        return result
