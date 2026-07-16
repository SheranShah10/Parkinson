import os
import json
import pandas as pd
import hashlib
from datetime import datetime

class FeatureExporter:
    def __init__(self, store_dir, metadata_dir):
        self.store_dir = store_dir
        self.metadata_dir = metadata_dir
        
    def export_modality(self, df, prefix, name):
        cols = [c for c in df.columns if c.startswith(prefix) or c in ['PATNO', 'EVENT_ID']]
        if not cols: return
        subset = df[cols]
        path = os.path.join(self.store_dir, f"{name}_features.parquet")
        subset.to_parquet(path, index=False)
        return self._hash(path, subset)
        
    def _hash(self, path, df):
        with open(path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()
        return {
            'Hash': file_hash,
            'Rows': len(df),
            'Cols': len(df.columns),
            'Timestamp': datetime.utcnow().isoformat()
        }
