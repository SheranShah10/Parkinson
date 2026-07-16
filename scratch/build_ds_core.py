import os

base_dir = "C:/Users/Sheran/Desktop/Parkinson"
dirs = [
    "configs/datasets",
    "src/datasets",
    "src/dataloaders",
    "src/samplers",
    "src/cross_validation"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    with open(os.path.join(base_dir, d, "__init__.py"), "w") as f:
        f.write("")

# 1. Cross Validation Engine (Group K-Fold strict PATNO)
cv_code = """import pandas as pd
import numpy as np

class StratifiedGroupKFoldProxy:
    def __init__(self, n_splits=5, shuffle=True, random_state=42):
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state
        
    def split(self, df, group_col='PATNO', target_col='TARGET_NHY'):
        groups = df[group_col].unique()
        if self.shuffle:
            np.random.seed(self.random_state)
            np.random.shuffle(groups)
            
        fold_sizes = len(groups) // self.n_splits
        folds = []
        for i in range(self.n_splits):
            start = i * fold_sizes
            end = start + fold_sizes if i != self.n_splits - 1 else len(groups)
            val_groups = set(groups[start:end])
            
            train_idx = df[~df[group_col].isin(val_groups)].index.tolist()
            val_idx = df[df[group_col].isin(val_groups)].index.tolist()
            folds.append((train_idx, val_idx))
            
        return folds
"""
with open(os.path.join(base_dir, "src/cross_validation/stratified_group_kfold.py"), "w") as f: f.write(cv_code)

# 2. Base Loaders & Modalities
loader_code = """import pandas as pd
import numpy as np

class BaseDataLoader:
    def __init__(self, df, batch_size=32, shuffle=True):
        self.df = df
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.indices = np.arange(len(df))
        if self.shuffle:
            np.random.shuffle(self.indices)
            
    def __iter__(self):
        for i in range(0, len(self.df), self.batch_size):
            batch_idx = self.indices[i:i+self.batch_size]
            yield self.df.iloc[batch_idx]
            
class GraphDatasetBuilder:
    def build_patient_graph(self, df):
        # Mocks PyG structure
        nodes = df['PATNO'].unique()
        edges = [] # Fully connected mockup for validation
        for i in range(min(100, len(nodes))):
            for j in range(i+1, min(100, len(nodes))):
                edges.append((nodes[i], nodes[j]))
        return {'Nodes': len(nodes), 'Edges': len(edges)}
        
class TemporalSequenceBuilder:
    def build_lag_sequence(self, df, horizon=1):
        df_sorted = df.sort_values(['PATNO', 'EVENT_ID'])
        num_cols = df_sorted.select_dtypes(include=np.number).columns.tolist()
        res = df_sorted.copy()
        # Strictly ensuring no +horizon leakage by only taking shift(horizon)
        for c in num_cols:
            if not c.startswith('TARGET_'):
                res[f'{c}_lag{horizon}'] = df_sorted.groupby('PATNO')[c].shift(horizon)
        return res
"""
with open(os.path.join(base_dir, "src/dataloaders/loaders.py"), "w") as f: f.write(loader_code)

print("Scaffolded Phase 6.3 Core Components.")
