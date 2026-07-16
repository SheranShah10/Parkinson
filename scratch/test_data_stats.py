import os
import pandas as pd
import numpy as np

def get_temporal_data():
    input_dir = "data" if os.path.exists("data") else "c:/Users/Sheran/Desktop/Parkinson/data"
    fs_path = os.path.join(input_dir, "master_features.parquet")
    df = pd.read_parquet(fs_path)
    
    event_order = {'BL':0, 'V01':1, 'V02':2, 'V03':3, 'V04':4, 'V05':5, 'V06':6, 'V07':7, 'V08':8, 'V09':9, 'V10':10, 'V11':11, 'V12':12, 'V13':13, 'V14':14, 'V15':15, 'V16':16, 'V17':17, 'V18':18}
    df['EVENT_IDX'] = df['EVENT_ID'].map(event_order)
    df = df.dropna(subset=['EVENT_IDX']).sort_values(['PATNO', 'EVENT_IDX'])
    
    # Calculate lengths
    lengths = df.groupby('PATNO').size()
    
    print(f"Total Patients: {len(lengths)}")
    print(f"Min Visits: {lengths.min()}")
    print(f"Max Visits: {lengths.max()}")
    print(f"Mean Visits: {lengths.mean():.2f}")
    print(f"Median Visits: {lengths.median()}")
    
    short_seqs = (lengths <= 2).sum()
    print(f"Patients with 1-2 visits: {short_seqs} ({short_seqs/len(lengths)*100:.2f}%)")

if __name__ == '__main__':
    get_temporal_data()
