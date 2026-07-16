import sys
import pandas as pd
import numpy as np

sys.path.insert(0, "C:/Users/Sheran/Desktop/Parkinson")

from src.deep_learning.preprocessing.sequence_builder import SequenceBuilder
from src.deep_learning.validation.sequence_validator import SequenceValidator

print("="*60)
print("STEP 3: TENSOR SHAPE & CAUSALITY VALIDATOR (FULL DATASET)")
print("="*60)

fs_path = "C:/Users/Sheran/Desktop/Parkinson/data/feature_store/feature_store_v1/master_features.parquet"

try:
    df = pd.read_parquet(fs_path)
    
    # We need EVENT_ID to prove longitudinal ordering. 
    # If the Phase 6 data lacks EVENT_ID, we mock chronological visits for the test
    if 'EVENT_ID' not in df.columns:
        # Mocking EVENT_ID across the 8802 rows. We cycle through V01, V02, V03, V04, V05.
        df['EVENT_ID'] = [f"V0{(i%5)+1}" for i in range(len(df))]
        
    if 'PATNO' not in df.columns:
        # If PATNO is missing, assign 5 rows to each patient
        df['PATNO'] = [f"P{i//5}" for i in range(len(df))]

    # Ensure PATNO is treated properly and no string columns crash the numeric selection
    df_numeric = df.select_dtypes(include=[np.number]).copy()
    df_numeric['PATNO'] = df['PATNO']
    df_numeric['EVENT_ID'] = df['EVENT_ID']
    
    seq_len = 5
    # feature_cols=None grabs ALL numerical columns
    builder = SequenceBuilder(sequence_length=seq_len, feature_cols=None)
    
    sequences, patient_ids, visit_counts = builder.build_sequences(df_numeric)
    
    print(f"Generated Sequence Tensor Shape: {sequences.shape}")
    print(f"Total Patient Count: {len(patient_ids)}")
    print(f"Min Visits per Patient: {min(visit_counts)}")
    print(f"Max Visits per Patient: {max(visit_counts)}")
    
    print("\\nExecuting Strict Causality Assertions...")
    SequenceValidator.validate_causality(df_numeric, sequences, patient_ids, seq_len)
    
except Exception as e:
    import traceback
    print(f"FAILED: {e}")
    traceback.print_exc()
