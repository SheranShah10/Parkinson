import pandas as pd
import numpy as np
import os

def analyze_time_missingness(df, reports_dir):
    print("Analyzing Time-Aware Missingness...")
    
    report = ["# Time-Aware Missingness Report\n"]
    if 'EVENT_ID' in df.columns:
        visits = ['BL', 'V04', 'V06', 'V08']
        for v in visits:
            df_v = df[df['EVENT_ID'] == v]
            if len(df_v) > 0:
                miss_pct = df_v.isnull().sum().sum() / df_v.size * 100
                report.append(f"## Missingness at {v}")
                report.append(f"- Patients: {len(df_v)}")
                report.append(f"- Overall Missingness: {miss_pct:.2f}%")
            
    with open(os.path.join(reports_dir, 'time_missingness_report.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
