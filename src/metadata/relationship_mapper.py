"""
Relationship Mapper Module
"""
from typing import List, Dict, Any

class RelationshipMapper:
    PRIMARY_KEYS = ["PATNO"]
    VISIT_KEYS = ["EVENT_ID", "INFODT", "VISIT", "VISIT_ID"]
    
    def map_relationships(self, datasets: List[Dict[str, Any]]) -> Dict[str, Any]:
        relationships = []
        for ds in datasets:
            cols = [c.upper() for c in ds.get("columns_list", [])]
            pks = [k for k in self.PRIMARY_KEYS if k in cols]
            vks = [k for k in self.VISIT_KEYS if k in cols]
            
            rel = {
                "name": ds["name"],
                "primary_keys": pks,
                "visit_keys": vks,
                "merge_keys": pks + vks
            }
            relationships.append(rel)
            
        return {"relationships": relationships}
        
    def generate_mermaid_er(self, relationships: List[Dict[str, Any]]) -> str:
        lines = ["erDiagram"]
        lines.append('    MASTER_COHORT {')
        lines.append('        string PATNO PK')
        lines.append('        string EVENT_ID PK')
        lines.append('    }')
        
        for rel in relationships:
            name = rel["name"].split('.')[0].replace(' ', '_').replace('-', '_')
            name = "".join([c for c in name if c.isalnum() or c == '_'])
            
            if rel["primary_keys"] and rel["visit_keys"]:
                lines.append(f'    MASTER_COHORT ||--o{{ {name} : "PATNO, EVENT_ID"')
            elif rel["primary_keys"]:
                lines.append(f'    MASTER_COHORT ||--o| {name} : "PATNO"')
                
            lines.append(f'    {name} {{')
            for pk in rel["primary_keys"]:
                lines.append(f'        string {pk} FK')
            for vk in rel["visit_keys"]:
                lines.append(f'        string {vk} FK')
            lines.append('    }')
            
        return "\n".join(lines)
