import pandas as pd

print("="*60)
print("STEP 2B: PLAUSIBILITY CHECK ON PHASE 6 DATA")
print("="*60)

fs_path = "C:/Users/Sheran/Desktop/Parkinson/data/feature_store/feature_store_v1/master_features.parquet"
df = pd.read_parquet(fs_path)

col_to_check = 'SAA_TSmax_24h_Rep1'
if col_to_check in df.columns:
    print(f"\\nColumn: {col_to_check}")
    print(f"Min: {df[col_to_check].min():.4f}")
    print(f"Max: {df[col_to_check].max():.4f}")
    print(f"Mean: {df[col_to_check].mean():.4f}")
    
    negatives = (df[col_to_check] < 0).sum()
    print(f"Negative values count: {negatives} (Should be 0 for Biospecimen assays)")
else:
    print(f"Column {col_to_check} not found.")

updrs_col = 'NP3TOT'
if updrs_col in df.columns:
    print(f"\\nColumn: {updrs_col} (UPDRS Part III Motor Score)")
    print(f"Min: {df[updrs_col].min()} (Should be >= 0)")
    print(f"Max: {df[updrs_col].max()} (Should be <= 132)")
    print(f"Mean: {df[updrs_col].mean():.2f}")
    negatives_updrs = (df[updrs_col] < 0).sum()
    print(f"Negative values count: {negatives_updrs}")
else:
    print(f"Column {updrs_col} not found.")
