import pandas as pd
import os

print("--- STEP 1: AUDITING PHASE 6 FEATURE STORE ---")

feature_store_path = "C:/Users/Sheran/Desktop/Parkinson/data/feature_store/feature_store_v1/master_features.parquet"
df = pd.read_parquet(feature_store_path)

print(f"Loaded master_features.parquet.")
print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)[:10]} ...")

# Check for actual data variance
numeric_df = df.select_dtypes(include=['float64', 'int64'])
variances = numeric_df.var()

print("\\nInspecting Variances of 3 Random Numerical Columns:")
sample_vars = variances.dropna().sample(3, random_state=42)
for col, var in sample_vars.items():
    print(f"  - {col}: Variance = {var:.4f}")

# Assertion Check
print("\\nExecuting Assertions...")
assert not numeric_df.empty, "Numeric DataFrame is empty! Data might be completely faked/missing."
assert (variances > 0).any(), "Zero variance across all numerical columns! Data is static/fake."
assert len(df) > 1000, "Insufficient row count, data is likely stubbed."
print("[PASS] Phase 6 Feature Store contains real, computed variance. It is not a stub.")
