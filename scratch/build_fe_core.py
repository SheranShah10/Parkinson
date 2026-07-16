import os

base_dir = "C:/Users/Sheran/Desktop/Parkinson"
dirs = [
    "src/feature_engineering",
    "configs/features",
    "tests/test_feature_engineering",
    "data/feature_store/feature_store_v1"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)

with open(os.path.join(base_dir, "src/feature_engineering/__init__.py"), "w") as f:
    f.write("")

# 1. Scaling Framework
scaling_code = """import pandas as pd
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
"""
with open(os.path.join(base_dir, "src/feature_engineering/scaling.py"), "w") as f: f.write(scaling_code)

# 2. Encoding Framework
encoding_code = """import pandas as pd
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
"""
with open(os.path.join(base_dir, "src/feature_engineering/encoding.py"), "w") as f: f.write(encoding_code)

# 3. Validation Framework
validation_code = """import pandas as pd
import numpy as np

def validate_features(df, targets=['TARGET_NHY']):
    report = []
    report.append("# Feature Validation Report")
    
    # 1. Constants
    constants = [c for c in df.columns if df[c].nunique(dropna=False) <= 1]
    if constants:
        report.append(f"\\n## Constant Features ({len(constants)})")
        report.append(", ".join(constants[:20]) + ("..." if len(constants)>20 else ""))
        
    # 2. NaN pct
    nan_pct = df.isnull().mean()
    high_nan = nan_pct[nan_pct > 0.9]
    if not high_nan.empty:
        report.append(f"\\n## High Missingness (>90%) ({len(high_nan)})")
        report.append(", ".join(high_nan.index[:20]))
        
    # 3. Leakage
    leaks = [c for c in df.columns if 'TARGET_' in c and c not in targets]
    if leaks:
        report.append(f"\\n## Suspicious Target Leakage ({len(leaks)})")
        report.append(", ".join(leaks))
        
    return "\\n".join(report)
"""
with open(os.path.join(base_dir, "src/feature_engineering/feature_validator.py"), "w") as f: f.write(validation_code)


