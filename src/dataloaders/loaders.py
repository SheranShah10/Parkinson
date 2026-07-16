import pandas as pd
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
