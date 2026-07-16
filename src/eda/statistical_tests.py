import pandas as pd
import numpy as np
import os
try:
    from scipy.stats import skew, kurtosis
except:
    def skew(x): return 0
    def kurtosis(x): return 0

def run_tests(df, reports_dir):
    print("Running Statistical Assumptions...")
    num_cols = df.select_dtypes(include=np.number).columns.tolist()[:50]
    
    report = [
        "# Statistical Assumption Testing\n",
        "## Normality Proxies (Skewness/Kurtosis)"
    ]
    
    for c in num_cols:
        v = df[c].dropna().values
        if len(v) > 0:
            s = skew(v)
            k = kurtosis(v)
            if abs(s) > 1 or abs(k) > 3:
                report.append(f"- **{c}**: Non-normal (Skew: {s:.2f}, Kurtosis: {k:.2f}) -> Use non-parametric tests.")
                
    with open(os.path.join(reports_dir, 'statistical_assumptions.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
