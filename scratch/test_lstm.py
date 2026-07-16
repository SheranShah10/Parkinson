import os
import sys
sys.path.append('.')
import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence
from src.deep_learning.models.temporal_models import LSTM
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

def get_temporal_data():
    input_dir = "data" if os.path.exists("data") else "c:/Users/Sheran/Desktop/Parkinson/data"
    fs_path = None
    for root, dirs, files in os.walk(input_dir):
        if "master_features.parquet" in files:
            fs_path = os.path.join(root, "master_features.parquet")
            break
    
    # If not found locally, just generate a mocked sequence dataframe
    if not fs_path:
        print("Using dummy generated data for local test...")
        np.random.seed(42)
        n_patients = 100
        data = []
        # Create sequences of random lengths between 1 and 5
        event_map = {0:'BL', 1:'V04', 2:'V06', 3:'V08', 4:'V10'}
        for p in range(n_patients):
            seq_len = np.random.randint(1, 6)
            for s in range(seq_len):
                row = {'PATNO': p, 'EVENT_ID': event_map[s], 'NP3TOT': np.random.rand() * 50, 'NHY': np.random.choice([0,1,2,3])}
                for i in range(20): # 20 dummy features
                    row[f'FEAT_{i}'] = np.random.randn()
                data.append(row)
        df = pd.DataFrame(data)
    else:
        df = pd.read_parquet(fs_path)

    # EVENT_ID mapping for strict temporal sorting
    event_order = {'BL':0, 'V01':1, 'V02':2, 'V03':3, 'V04':4, 'V05':5, 'V06':6, 'V07':7, 'V08':8, 'V09':9, 'V10':10, 'V11':11, 'V12':12, 'V13':13, 'V14':14, 'V15':15, 'V16':16, 'V17':17, 'V18':18}
    
    # Filter only recognizable sequential events
    df['EVENT_IDX'] = df['EVENT_ID'].map(event_order)
    df = df.dropna(subset=['EVENT_IDX'])
    
    # SORTING: Ensure strictly causal chronological ordering
    df = df.sort_values(['PATNO', 'EVENT_IDX'])

    # LEAKAGE PURGE (Tested and Confirmed)
    leaky_patterns = ['NHY', 'NP3', 'TARGET_', 'MOTOR_SEVERITY', 'TEMPORAL_MOTOR_SLOPE', 'PD_DX', 'CLINI_', 'MDS-U_'] 
    leaky_cols = [c for c in df.columns if any(pat in c.upper() for pat in leaky_patterns)]
    
    df_features = df.drop(columns=leaky_cols + ['EVENT_ID', 'EVENT_IDX'], errors='ignore')
    
    # Keep only numeric
    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    df_features = df_features[numeric_cols]
    
    # Extract PATNO to group
    df_features['PATNO'] = df['PATNO'].values
    
    # We will predict the NEXT visit's NP3TOT, or just the CURRENT visit's NP3TOT
    # For now, to match Tier 2, we just take the sequence and predict the final NP3TOT
    # Since this is a smoke test, we just use the raw NP3TOT column from df.
    df_features['TARGET_NP3'] = df['NP3TOT'].values
    
    # Simple imputation and scaling for features (excluding PATNO and TARGET)
    feature_cols = [c for c in df_features.columns if c not in ['PATNO', 'TARGET_NP3']]
    
    # Impute/scale locally for smoke test
    X_raw = df_features[feature_cols].values
    X_raw = SimpleImputer(strategy='median').fit_transform(X_raw)
    X_raw = StandardScaler().fit_transform(X_raw)
    
    df_features[feature_cols] = X_raw
    df_features = df_features.dropna(subset=['TARGET_NP3'])
    
    # GROUP BY PATIENT INTO SEQUENCES
    sequences = []
    targets = []
    
    for patno, group in df_features.groupby('PATNO'):
        # Ensure it's sorted just in case
        # Features
        seq = torch.tensor(group[feature_cols].values, dtype=torch.float32)
        # Target: The final visit's NP3 score
        target = torch.tensor(group['TARGET_NP3'].values[-1], dtype=torch.float32)
        
        sequences.append(seq)
        targets.append(target)
        
    return sequences, targets, len(feature_cols)

# Custom Collate Function for DataLoader
def collate_fn(batch):
    sequences, targets = zip(*batch)
    # Calculate lengths before padding
    lengths = torch.tensor([len(seq) for seq in sequences], dtype=torch.int64)
    # Pad sequences to max length in the batch (adds 0s at the end)
    padded_seqs = pad_sequence(sequences, batch_first=True, padding_value=0.0)
    targets = torch.tensor(targets, dtype=torch.float32)
    return padded_seqs, targets, lengths

class ParkinsonSeqDataset(Dataset):
    def __init__(self, sequences, targets):
        self.sequences = sequences
        self.targets = targets
    def __len__(self): return len(self.sequences)
    def __getitem__(self, idx): return self.sequences[idx], self.targets[idx]

def run_smoke_test():
    print("--- 1. BUILDING SEQUENCE DATA ---")
    sequences, targets, num_features = get_temporal_data()
    print(f"Total Sequences: {len(sequences)}, Feature Dim: {num_features}")
    
    dataset = ParkinsonSeqDataset(sequences, targets)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True, collate_fn=collate_fn)
    
    print("\n--- 2. LSTM INSTANTIATION TEST ---")
    model = LSTM(input_dim=num_features, hidden_dim=64, num_layers=2, output_dim=1, dropout=0.2)
    
    # Get one batch
    batch_x, batch_y, lengths = next(iter(dataloader))
    print(f"Batch X shape: {batch_x.shape} -> [Batch, MaxTime, Features]")
    print(f"Lengths: {lengths.tolist()}")
    
    # Test forward pass
    try:
        out = model(batch_x, lengths)
        print(f"✅ LSTM Forward Pass Passed! Expected output: [32, 1], Actual: {list(out.shape)}")
    except Exception as e:
        print(f"🚨 LSTM Forward Pass Failed: {e}")
        return
        
    print("\n--- 3. LSTM SMOKE TEST (LOSS TRACE) ---")
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    model.train()
    for epoch in range(3):
        total_loss = 0
        for batch_x, batch_y, lengths in dataloader:
            optimizer.zero_grad()
            out = model(batch_x, lengths).squeeze()
            loss = criterion(out, batch_y)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
        print(f"Epoch {epoch+1}/3 - MSE Loss: {total_loss/len(dataloader):.4f}")

if __name__ == '__main__':
    run_smoke_test()
