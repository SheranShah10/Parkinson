import pandas as pd
import numpy as np

class BaseSelector:
    def __init__(self):
        self.is_fitted = False
        self.selected_features = []
        
    def fit(self, X, y=None):
        raise NotImplementedError
        
    def transform(self, X):
        if not self.is_fitted:
            raise ValueError("Selector not fitted.")
        valid_cols = [c for c in self.selected_features if c in X.columns]
        return X[valid_cols]
        
    def fit_transform(self, X, y=None):
        return self.fit(X, y).transform(X)
        
    def save(self, path):
        pass
        
    def load(self, path):
        pass
