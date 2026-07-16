import pandas as pd
import numpy as np
import os

def detect_leakage(df, reports_dir):
    print("Detecting Target Leakage...")
    targets = [c for c in df.columns if c.startswith('TARGET_')]
    identifiers = ['PATNO', 'EVENT_ID', 'INFODT']
    
    leakage_report = [
        "# Target Leakage Detection Report\n",
        "## Identifier Leakage",
        "The following variables are strict identifiers and must NOT be used as predictors:"
    ]
    for i in identifiers:
        if i in df.columns:
            leakage_report.append(f"- {i}")
            
    leakage_report.append("\n## High Correlation Leakage (>0.99)")
    leakage_report.append("The following features exhibit >0.99 correlation with targets and represent potential leakage:")
    
    # Calculate correlations efficiently
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in targets + identifiers]
    
    found_leakage = False
    for t in targets:
        if t not in df.columns or df[t].dtype not in [np.float64, np.int64, float, int]: continue
        y = df[t].values
        mask_y = ~np.isnan(y)
        for c in numeric_cols:
            x = df[c].values
            mask_x = ~np.isnan(x)
            mask = mask_y & mask_x
            if mask.sum() > 10:
                corr = np.corrcoef(x[mask], y[mask])[0, 1]
                if abs(corr) > 0.99:
                    leakage_report.append(f"- **{c}** correlates with {t} ({corr:.4f})")
                    found_leakage = True
                    
    if not found_leakage:
        leakage_report.append("No features exceeded the 0.99 correlation threshold.")
        
    leakage_report.append("\n## Future-Derived Variables")
    leakage_report.append("Variables containing 'DELTA', 'CHANGE', or derived targets from future dates must be excluded during cross-sectional prediction tasks.")
    
    with open(os.path.join(reports_dir, 'leakage_report.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(leakage_report))
