"""
Registry Module

Responsibility: Maintain the central state of datasets.
"""
import os
import hashlib
from typing import Dict, Any, List

class DatasetRegistry:
    def __init__(self):
        self.entries: List[Dict[str, Any]] = []
        
    def _compute_hash(self, filepath: str) -> str:
        h = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            return h.hexdigest()
        except:
            return ""

    def register(self, filepath: str, validation: Dict[str, Any], schema: Dict[str, Any], base_dir: str):
        file_stats = os.stat(filepath)
        rel_path = os.path.relpath(filepath, base_dir)
        
        entry = {
            "dataset_name": os.path.basename(filepath),
            "location": rel_path,
            "size_bytes": file_stats.st_size,
            "is_valid": validation.get("is_valid", False),
            "validation_errors": validation.get("error_message", ""),
            "schema_status": schema.get("status", "unknown"),
            "found_identifiers": schema.get("found_identifiers", []),
            "file_hash": self._compute_hash(filepath)
        }
        self.entries.append(entry)
        
    def get_registry(self) -> List[Dict[str, Any]]:
        return self.entries
