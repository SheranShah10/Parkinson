import pandas as pd
import numpy as np

class CustomScaler:
    def __init__(self, method='standard'):
        self.method = method
        self.params = {}
        self.is_fitted = False
        
    def fit(self, X):
        for col in X.columns:
            vals = X[col].dropna().values
            if len(vals) == 0:
                self.params[col] = {'mean': 0, 'scale': 1, 'min': 0}
                continue
                
            if self.method == 'standard':
                self.params[col] = {'mean': np.mean(vals), 'scale': np.std(vals) + 1e-10}
            elif self.method == 'robust':
                q25, q50, q75 = np.percentile(vals, [25, 50, 75])
                iqr = q75 - q25
                self.params[col] = {'mean': q50, 'scale': iqr if iqr > 0 else 1.0}
            elif self.method == 'minmax':
                vmin, vmax = np.min(vals), np.max(vals)
                rng = vmax - vmin
                self.params[col] = {'min': vmin, 'scale': rng if rng > 0 else 1.0}
        self.is_fitted = True
        return self
        
    def transform(self, X):
        if not self.is_fitted: raise ValueError("Scaler not fitted.")
        X_scaled = X.copy()
        for col in X.columns:
            if col in self.params:
                p = self.params[col]
                if self.method in ['standard', 'robust']:
                    X_scaled[col] = (X_scaled[col] - p['mean']) / p['scale']
                elif self.method == 'minmax':
                    X_scaled[col] = (X_scaled[col] - p['min']) / p['scale']
        return X_scaled
        
    def fit_transform(self, X):
        return self.fit(X).transform(X)
