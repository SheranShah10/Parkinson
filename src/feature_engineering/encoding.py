import pandas as pd
import numpy as np

class CustomEncoder:
    def __init__(self, method='onehot'):
        self.method = method
        self.mapping = {}
        self.is_fitted = False
        
    def fit(self, X, y=None):
        for col in X.columns:
            if self.method == 'ordinal':
                unique_vals = sorted(X[col].dropna().unique())
                self.mapping[col] = {v: i for i, v in enumerate(unique_vals)}
            elif self.method == 'frequency':
                counts = X[col].value_counts(normalize=True).to_dict()
                self.mapping[col] = counts
            elif self.method == 'onehot':
                self.mapping[col] = sorted(X[col].dropna().unique().tolist())
            elif self.method == 'target' and y is not None:
                means = pd.DataFrame({'x': X[col], 'y': y}).groupby('x')['y'].mean().to_dict()
                global_mean = np.mean(y)
                self.mapping[col] = {'means': means, 'global': global_mean}
        self.is_fitted = True
        return self
        
    def transform(self, X):
        if not self.is_fitted: raise ValueError("Encoder not fitted.")
        if self.method == 'onehot':
            out = []
            for col in X.columns:
                if col in self.mapping:
                    for val in self.mapping[col]:
                        out.append((X[col] == val).astype(float).rename(f"{col}_{val}"))
            if not out: return X.copy()
            return pd.concat(out, axis=1)
            
        X_enc = X.copy()
        for col in X.columns:
            if col in self.mapping:
                if self.method == 'ordinal':
                    X_enc[col] = X_enc[col].map(self.mapping[col]).fillna(-1)
                elif self.method == 'frequency':
                    X_enc[col] = X_enc[col].map(self.mapping[col]).fillna(0)
                elif self.method == 'target':
                    d = self.mapping[col]
                    X_enc[col] = X_enc[col].map(d['means']).fillna(d['global'])
        return X_enc
