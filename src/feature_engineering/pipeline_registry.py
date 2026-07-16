import os
import pandas as pd
import json

class FeatureRegistry:
    def __init__(self, metadata_dir):
        self.metadata_dir = metadata_dir
        self.registry = []
        
    def add_feature(self, name, parents, method, tag, is_leakage_safe=True):
        self.registry.append({
            'Feature_Name': name,
            'Parents': parents,
            'Engineering_Method': method,
            'Tags': tag,
            'Leakage_Safe': is_leakage_safe
        })
        
    def export(self):
        df = pd.DataFrame(self.registry)
        df.to_csv(os.path.join(self.metadata_dir, 'engineered_feature_registry.csv'), index=False)
        with open(os.path.join(self.metadata_dir, 'engineered_feature_registry.json'), 'w') as f:
            json.dump(self.registry, f, indent=4)
