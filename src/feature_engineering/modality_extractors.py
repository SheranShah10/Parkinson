import pandas as pd
import numpy as np

def generate_clinical_features(df, registry):
    print("Generating Clinical Features...")
    df_out = df.copy()
    if 'NP1RTOT' in df.columns:
        df_out['CLINICAL_NonMotor_Severity'] = df['NP1RTOT'] * 1.5
        registry.add_feature('CLINICAL_NonMotor_Severity', ['NP1RTOT'], 'Multiplication', 'Clinical,NonMotor')
    return df_out

def generate_motor_features(df, registry):
    print("Generating Motor Features...")
    df_out = df.copy()
    if 'NP3TOT' in df.columns:
        df_out['MOTOR_Severity_Score'] = df['NP3TOT']
        registry.add_feature('MOTOR_Severity_Score', ['NP3TOT'], 'Identity', 'Motor,Clinical')
    return df_out

def generate_temporal_features(df, registry):
    print("Generating Temporal Features...")
    df_out = df.copy()
    if 'EVENT_ID' in df.columns and 'NP3TOT' in df.columns and 'PATNO' in df.columns:
        df_out = df_out.sort_values(['PATNO', 'EVENT_ID'])
        df_out['TEMPORAL_Motor_Lag1'] = df_out.groupby('PATNO')['NP3TOT'].shift(1)
        df_out['TEMPORAL_Motor_Slope'] = df_out['NP3TOT'] - df_out['TEMPORAL_Motor_Lag1'].fillna(0)
        registry.add_feature('TEMPORAL_Motor_Lag1', ['NP3TOT'], 'Time Shift', 'Temporal')
        registry.add_feature('TEMPORAL_Motor_Slope', ['NP3TOT', 'TEMPORAL_Motor_Lag1'], 'Difference', 'Temporal')
    return df_out
