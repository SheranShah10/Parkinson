import pandas as pd
import numpy as np
import os

def analyze_stability(df, reports_dir):
    print("Analyzing Feature Stability...")
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    num_cols = [c for c in num_cols if c not in ['PATNO'] and not c.startswith('TARGET_')]
    
    results = []
    for c in num_cols:
        col_mean = df[c].mean()
        col_var = df[c].var()
        cv = np.sqrt(col_var) / abs(col_mean) if col_mean != 0 else np.nan
        
        # Shift analysis
        if 'EVENT_ID' in df.columns:
            bl = df[df['EVENT_ID'] == 'BL'][c].mean()
            v04 = df[df['EVENT_ID'] == 'V04'][c].mean()
            shift = (v04 - bl) / abs(bl) if bl != 0 and not np.isnan(bl) and not np.isnan(v04) else np.nan
        else:
            shift = np.nan
            
        results.append({
            'Feature': c,
            'Overall_Mean': col_mean,
            'Temporal_Variance': col_var,
            'Coefficient_of_Variation': cv,
            'Baseline_vs_V04_Shift': shift
        })
        
    df_res = pd.DataFrame(results)
    df_res.to_csv(os.path.join(reports_dir, 'feature_stability.csv'), index=False)
    
    report = [
        "# Feature Stability Report\n",
        "## Summary",
        f"- Total features analyzed: {len(num_cols)}",
        f"- Features with zero variance: {df_res['Temporal_Variance'].eq(0).sum()}",
        f"- Median Coefficient of Variation: {df_res['Coefficient_of_Variation'].median():.4f}",
        "\nDetailed stability metrics have been saved to `feature_stability.csv`."
    ]
    with open(os.path.join(reports_dir, 'feature_stability_report.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
