import pandas as pd
import numpy as np

fs_path = "C:/Users/Sheran/Desktop/Parkinson/data/feature_store/feature_store_v1/master_features.parquet"
df = pd.read_parquet(fs_path)

print("Columns in Phase 6 Data:")
print("EVENT_ID present?", 'EVENT_ID' in df.columns)
print("PATNO present?", 'PATNO' in df.columns)

if 'PATNO' in df.columns:
    vc = df['PATNO'].value_counts()
    print("PATNO value counts summary:")
    print(vc.describe())
    print("Top 5 PATNO counts:")
    print(vc.head())
    print("Bottom 5 PATNO counts:")
    print(vc.tail())
