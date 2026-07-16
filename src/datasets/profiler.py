"""
Dataset Profiler Module

Responsibility: Extract metadata, dimensions, memory usage, and basic quality metrics
from various dataset types without modifying them.
"""

import os
import json
import zipfile
from typing import Dict, Any, List
import pandas as pd
import numpy as np

class DatasetProfiler:
    """Base profiler for datasets."""
    
    @staticmethod
    def profile(filepath: str, ext: str) -> Dict[str, Any]:
        """Route to appropriate profiler based on extension."""
        file_size = os.path.getsize(filepath)
        base_meta = {
            "file_name": os.path.basename(filepath),
            "absolute_path": os.path.abspath(filepath),
            "extension": ext.lower(),
            "file_size_bytes": file_size,
            "status": "success",
            "error_msg": None
        }

        try:
            if ext.lower() in ['.csv', '.tsv', '.txt']:
                sep = '\t' if ext.lower() in ['.tsv', '.txt'] else ','
                meta = TabularProfiler.profile(filepath, sep=sep)
            elif ext.lower() in ['.xls', '.xlsx']:
                meta = TabularProfiler.profile_excel(filepath)
            elif ext.lower() == '.parquet':
                meta = TabularProfiler.profile_parquet(filepath)
            elif ext.lower() == '.json':
                meta = JsonProfiler.profile(filepath)
            elif ext.lower() == '.zip':
                meta = ZipProfiler.profile(filepath)
            else:
                meta = {"status": "unsupported_format"}
        except Exception as e:
            meta = {"status": "error", "error_msg": str(e)}

        base_meta.update(meta)
        return base_meta


class TabularProfiler:
    """Profiler for tabular data formats (CSV, TSV, Parquet, Excel)."""
    
    @staticmethod
    def _extract_metrics(df: pd.DataFrame) -> Dict[str, Any]:
        memory_usage = df.memory_usage(deep=True).sum()
        missing_counts = df.isnull().sum()
        
        patno_count = df['PATNO'].nunique() if 'PATNO' in df.columns else 0
        event_count = df['EVENT_ID'].nunique() if 'EVENT_ID' in df.columns else 0
        
        # Identify date and target columns
        date_cols = [c for c in df.columns if 'date' in c.lower() or 'dt' in c.lower()]
        target_cols = [c for c in df.columns if 'updrs' in c.lower() or 'status' in c.lower() or 'pd_state' in c.lower()]
        
        # Determine cardinality and empty/constant cols
        unique_counts = df.nunique()
        empty_cols = list(missing_counts[missing_counts == len(df)].index)
        constant_cols = list(unique_counts[unique_counts == 1].index)
        high_cardinality = list(unique_counts[unique_counts > (len(df) * 0.9)].index)

        # Remove primary keys from high cardinality if they are standard identifiers
        potential_pks = [c for c in high_cardinality if 'id' in c.lower() or 'no' in c.lower()]
        
        return {
            "num_rows": len(df),
            "num_columns": len(df.columns),
            "column_names": list(df.columns),
            "column_dtypes": {str(k): str(v) for k, v in df.dtypes.items()},
            "estimated_memory_bytes": int(memory_usage),
            "duplicate_rows": int(df.duplicated().sum()),
            "total_missing_values": int(missing_counts.sum()),
            "missing_percentage": float((missing_counts.sum() / (len(df) * len(df.columns))) * 100) if len(df) > 0 and len(df.columns) > 0 else 0,
            "unique_patno_count": patno_count,
            "unique_event_id_count": event_count,
            "date_columns": date_cols,
            "target_related_columns": target_cols,
            "empty_columns": empty_cols,
            "constant_columns": constant_cols,
            "potential_primary_keys": potential_pks,
            "dataset_type": "tabular"
        }

    @staticmethod
    def profile(filepath: str, sep: str = ',') -> Dict[str, Any]:
        df = pd.read_csv(filepath, sep=sep, low_memory=False)
        return TabularProfiler._extract_metrics(df)

    @staticmethod
    def profile_excel(filepath: str) -> Dict[str, Any]:
        df = pd.read_excel(filepath)
        return TabularProfiler._extract_metrics(df)

    @staticmethod
    def profile_parquet(filepath: str) -> Dict[str, Any]:
        df = pd.read_parquet(filepath)
        return TabularProfiler._extract_metrics(df)


class JsonProfiler:
    """Profiler for JSON files."""
    
    @staticmethod
    def profile(filepath: str) -> Dict[str, Any]:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            num_rows = len(data)
            num_columns = len(data[0].keys()) if num_rows > 0 and isinstance(data[0], dict) else 0
        elif isinstance(data, dict):
            num_rows = 1
            num_columns = len(data.keys())
        else:
            num_rows = 0
            num_columns = 0
            
        return {
            "num_rows": num_rows,
            "num_columns": num_columns,
            "dataset_type": "json"
        }

class ZipProfiler:
    """Profiler for ZIP archives (no extraction)."""
    
    @staticmethod
    def profile(filepath: str) -> Dict[str, Any]:
        with zipfile.ZipFile(filepath, 'r') as z:
            info_list = z.infolist()
            total_uncompressed = sum(info.file_size for info in info_list)
            filenames = [info.filename for info in info_list]
            
        return {
            "num_files_in_zip": len(filenames),
            "estimated_uncompressed_bytes": total_uncompressed,
            "zip_contents": filenames[:50],  # store up to 50 names to avoid massive bloat
            "dataset_type": "archive"
        }
