import pandas as pd
import numpy as np

def validate_features(df, targets=['TARGET_NHY']):
    report = []
    report.append("# Feature Validation Report")
    
    # 1. Constants
    constants = [c for c in df.columns if df[c].nunique(dropna=False) <= 1]
    if constants:
        report.append(f"\n## Constant Features ({len(constants)})")
        report.append(", ".join(constants[:20]) + ("..." if len(constants)>20 else ""))
        
    # 2. NaN pct
    nan_pct = df.isnull().mean()
    high_nan = nan_pct[nan_pct > 0.9]
    if not high_nan.empty:
        report.append(f"\n## High Missingness (>90%) ({len(high_nan)})")
        report.append(", ".join(high_nan.index[:20]))
        
    # 3. Leakage
    leaks = [c for c in df.columns if 'TARGET_' in c and c not in targets]
    if leaks:
        report.append(f"\n## Suspicious Target Leakage ({len(leaks)})")
        report.append(", ".join(leaks))
        
    return "\n".join(report)
