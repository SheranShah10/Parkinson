"""
Validator Module
"""
from typing import List, Dict, Any

class MetadataValidator:
    def validate(self, datasets: List[Dict[str, Any]]) -> List[str]:
        errors = []
        for ds in datasets:
            if ds["status"] != "valid":
                errors.append(f"[{ds['name']}] Status is {ds['status']}")
            
            cols = [c.upper() for c in ds.get("columns_list", [])]
            if "PATNO" not in cols:
                errors.append(f"[{ds['name']}] Missing PATNO primary key.")
                
            if len(cols) != len(set(cols)):
                errors.append(f"[{ds['name']}] Duplicate column names detected.")
                
        return errors
