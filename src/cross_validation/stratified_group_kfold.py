import pandas as pd
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
