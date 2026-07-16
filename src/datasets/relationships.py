"""
Relationships Module

Responsibility: Discover linkages between multiple datasets based on common keys.
"""

from typing import Dict, Any, List, Set

class RelationshipMapper:
    """Maps relationships across datasets."""
    
    COMMON_KEYS = ["PATNO", "EVENT_ID", "INFODT", "VISIT", "VISIT_MONTH", "PAG_NAME", "IMAGE_ID"]
    
    def __init__(self):
        self.dataset_keys: Dict[str, Set[str]] = {}
        
    def add_dataset(self, filename: str, column_names: List[str]):
        """Records the common keys present in a dataset."""
        if not column_names:
            return
            
        found_keys = {k for k in self.COMMON_KEYS if k in column_names}
        if found_keys:
            self.dataset_keys[filename] = found_keys
            
    def generate_relationship_map(self) -> List[Dict[str, Any]]:
        """Generates a graph-like mapping of how datasets can be joined."""
        edges = []
        files = list(self.dataset_keys.keys())
        
        for i in range(len(files)):
            for j in range(i + 1, len(files)):
                f1 = files[i]
                f2 = files[j]
                common = self.dataset_keys[f1].intersection(self.dataset_keys[f2])
                if common:
                    edges.append({
                        "source": f1,
                        "target": f2,
                        "keys": list(common)
                    })
        return edges
