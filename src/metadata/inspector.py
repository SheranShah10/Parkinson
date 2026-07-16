"""
Metadata Inspector Module
"""
import os
import pandas as pd
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DatasetInspector:
    def inspect(self, filepath: str) -> Dict[str, Any]:
        stats = {
            "name": os.path.basename(filepath),
            "path": filepath,
            "type": os.path.splitext(filepath)[1],
            "modality": self._infer_modality(filepath),
            "rows": 0,
            "columns": 0,
            "size_bytes": os.path.getsize(filepath),
            "missing_pct": 0.0,
            "columns_list": [],
            "dtypes": {},
            "status": "valid"
        }
        
        try:
            # We read nrows=100 for fast type inference and columns
            df_sample = pd.read_csv(filepath, low_memory=False, nrows=100)
            stats["columns"] = len(df_sample.columns)
            stats["columns_list"] = list(df_sample.columns)
            stats["dtypes"] = {k: str(v) for k, v in df_sample.dtypes.items()}
            
            # To get accurate rows & missing pct, we use chunks
            total_rows = 0
            total_missing = 0
            total_cells = 0
            
            for chunk in pd.read_csv(filepath, low_memory=False, chunksize=100000):
                total_rows += len(chunk)
                total_missing += chunk.isnull().sum().sum()
                total_cells += chunk.size
                
            stats["rows"] = total_rows
            if total_cells > 0:
                stats["missing_pct"] = round((total_missing / total_cells) * 100, 2)
                
        except Exception as e:
            stats["status"] = f"error: {str(e)}"
            
        return stats
        
    def _infer_modality(self, filepath: str) -> str:
        name = os.path.basename(filepath).lower()
        if 'motor' in name or 'updrs' in name: return "Motor"
        if 'datscan' in name or 'mri' in name: return "Imaging"
        if 'proteomic' in name or 'biospecimen' in name or 'saa' in name: return "Biospecimen/Omics"
        if 'sleep' in name or 'scopa' in name or 'upsit' in name: return "Non-Motor"
        if 'demographic' in name or 'status' in name or 'diagnosis' in name: return "Clinical/Demographics"
        return "Unknown"
