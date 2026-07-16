import os
import time
import math
import warnings
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import mean_squared_error, r2_score, f1_score, accuracy_score
import optuna

warnings.filterwarnings('ignore')

# Toggle Task Here
TASK_TYPE = 'classification'  # 'regression' or 'classification'

# =====================================================================
# 1. ARCHITECTURES
# =====================================================================
class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim, output_dim)
    def forward(self, x, lengths=None):
        if lengths is not None:
            x = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        out, _ = self.lstm(x)
        if lengths is not None:
            out, _ = pad_packed_sequence(out, batch_first=True)
            batch_size = out.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
        return self.fc(last_out)

class BiLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, bidirectional=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
    def forward(self, x, lengths=None):
        if lengths is not None:
            x = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        out, _ = self.lstm(x)
        if lengths is not None:
            out, _ = pad_packed_sequence(out, batch_first=True)
            batch_size = out.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
        return self.fc(last_out)

class GRU(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim, output_dim)
    def forward(self, x, lengths=None):
        if lengths is not None:
            x = pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        out, _ = self.gru(x)
        if lengths is not None:
            out, _ = pad_packed_sequence(out, batch_first=True)
            batch_size = out.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
        return self.fc(last_out)

class CausalConv1d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, dilation, dropout=0.2):
        super().__init__()
        self.left_padding = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, padding=0, dilation=dilation)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
    def forward(self, x):
        x_padded = F.pad(x, (self.left_padding, 0))
        return self.dropout(self.relu(self.conv(x_padded)))

class TCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, kernel_size=2, dropout=0.2):
        super().__init__()
        layers = []
        in_channels = input_dim
        for i in range(num_layers):
            dilation = 2 ** i
            layers.append(CausalConv1d(in_channels, hidden_dim, kernel_size, dilation, dropout))
            in_channels = hidden_dim
        self.network = nn.Sequential(*layers)
        self.fc = nn.Linear(hidden_dim, output_dim)
    def forward(self, x, lengths=None):
        x = x.transpose(1, 2)
        out = self.network(x)
        out = out.transpose(1, 2)
        if lengths is not None:
            batch_size = out.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
        return self.fc(last_out)

class CNN_LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, kernel_size=2, dropout=0.2):
        super().__init__()
        self.cnn = CausalConv1d(input_dim, hidden_dim, kernel_size, dilation=1, dropout=dropout)
        self.lstm = nn.LSTM(hidden_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim, output_dim)
    def forward(self, x, lengths=None):
        x_cnn = x.transpose(1, 2)
        out_cnn = self.cnn(x_cnn).transpose(1, 2)
        if lengths is not None:
            out_cnn = pack_padded_sequence(out_cnn, lengths, batch_first=True, enforce_sorted=False)
        out_lstm, _ = self.lstm(out_cnn)
        if lengths is not None:
            out_lstm, _ = pad_packed_sequence(out_lstm, batch_first=True)
            batch_size = out_lstm.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out_lstm.size(2)).unsqueeze(1)
            last_out = out_lstm.gather(1, idx).squeeze(1)
        else:
            last_out = out_lstm[:, -1, :]
        return self.fc(last_out)

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=50):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)[:, :pe[:, 1::2].shape[1]]
        self.register_buffer('pe', pe.unsqueeze(0)) 
    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class TransformerEncoderModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, nhead=4, dropout=0.2, max_len=50):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        self.pos_encoder = PositionalEncoding(hidden_dim, max_len)
        encoder_layers = nn.TransformerEncoderLayer(hidden_dim, nhead, hidden_dim*4, dropout, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layers, num_layers)
        self.fc = nn.Linear(hidden_dim, output_dim)
    def forward(self, x, lengths=None):
        seq_len, batch_size = x.size(1), x.size(0)
        x = self.pos_encoder(self.input_proj(x))
        causal_mask = torch.triu(torch.ones(seq_len, seq_len, dtype=torch.bool, device=x.device), diagonal=1)
        padding_mask = None
        if lengths is not None:
            padding_mask = torch.arange(seq_len).expand(batch_size, seq_len).to(lengths.device) >= lengths.unsqueeze(1)
        out = self.transformer(x, mask=causal_mask, src_key_padding_mask=padding_mask, is_causal=True)
        if lengths is not None:
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            return self.fc(out.gather(1, idx).squeeze(1))
        return self.fc(out[:, -1, :])

class TemporalTransformerModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, nhead=4, dropout=0.2, max_len=50):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        self.temporal_embedding = nn.Embedding(max_len, hidden_dim)
        encoder_layers = nn.TransformerEncoderLayer(hidden_dim, nhead, hidden_dim*4, dropout, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layers, num_layers)
        self.fc = nn.Linear(hidden_dim, output_dim)
    def forward(self, x, lengths=None):
        seq_len, batch_size = x.size(1), x.size(0)
        positions = torch.arange(0, seq_len, dtype=torch.long, device=x.device).unsqueeze(0).expand(batch_size, seq_len)
        x = self.input_proj(x) + self.temporal_embedding(positions)
        causal_mask = torch.triu(torch.ones(seq_len, seq_len, dtype=torch.bool, device=x.device), diagonal=1)
        padding_mask = None
        if lengths is not None:
            padding_mask = torch.arange(seq_len).expand(batch_size, seq_len).to(lengths.device) >= lengths.unsqueeze(1)
        out = self.transformer(x, mask=causal_mask, src_key_padding_mask=padding_mask, is_causal=True)
        if lengths is not None:
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            return self.fc(out.gather(1, idx).squeeze(1))
        return self.fc(out[:, -1, :])

# =====================================================================
# 2. DATA PREPARATION
# =====================================================================

class SeqDataset(Dataset):
    def __init__(self, sequences, targets):
        self.sequences = sequences
        self.targets = targets
    def __len__(self): return len(self.sequences)
    def __getitem__(self, idx): return self.sequences[idx], self.targets[idx]

def collate_fn(batch):
    sequences, targets = zip(*batch)
    lengths = torch.tensor([len(seq) for seq in sequences], dtype=torch.int64)
    padded_seqs = pad_sequence(sequences, batch_first=True, padding_value=0.0)
    
    if TASK_TYPE == 'classification':
        targets = torch.tensor(targets, dtype=torch.long)
    else:
        targets = torch.tensor(targets, dtype=torch.float32)
        
    return padded_seqs, targets, lengths

def build_temporal_dataset(df_path):
    print(f"Loading data from: {df_path}")
    df = pd.read_parquet(df_path)
    
    event_order = {'BL':0, 'V01':1, 'V02':2, 'V03':3, 'V04':4, 'V05':5, 'V06':6, 'V07':7, 'V08':8, 'V09':9, 'V10':10, 'V11':11, 'V12':12, 'V13':13, 'V14':14, 'V15':15, 'V16':16, 'V17':17, 'V18':18}
    df['EVENT_IDX'] = df['EVENT_ID'].map(event_order)
    df = df.dropna(subset=['EVENT_IDX']).sort_values(['PATNO', 'EVENT_IDX'])

    leaky_patterns = ['NHY', 'NP3', 'TARGET_', 'MOTOR_SEVERITY', 'TEMPORAL_MOTOR_SLOPE', 'PD_DX', 'CLINI_', 'MDS-U_'] 
    leaky_cols = [c for c in df.columns if any(pat in c.upper() for pat in leaky_patterns)]
    df_features = df.drop(columns=leaky_cols + ['EVENT_ID', 'EVENT_IDX'], errors='ignore')
    
    df_features = df_features.select_dtypes(include=[np.number])
    df_features['PATNO'] = df['PATNO'].values
    
    if TASK_TYPE == "classification":
        def collapse_nhy(raw_values):
            mapped = np.full(raw_values.shape, np.nan)
            valid = ~np.isnan(raw_values)
            v = raw_values[valid]
            out = np.select([v == 0, v == 1, v == 2, v >= 3], [0, 1, 2, 3], default=np.nan)
            mapped[valid] = out
            return mapped
        df_features['TARGET'] = collapse_nhy(df['NHY'].values.astype(float))
    else:
        df_features['TARGET'] = df['NP3TOT'].values
        
    feature_cols = [c for c in df_features.columns if c not in ['PATNO', 'TARGET']]
    
    visit_counts = df_features.groupby('PATNO').size()
    one_visit_pats = (visit_counts < 2).sum()
    print(f"Dropping {one_visit_pats} patients with < 2 visits.")
    
    valid_pats = visit_counts[visit_counts >= 2].index
    df_features = df_features[df_features['PATNO'].isin(valid_pats)].copy()
    
    missing_mask = df_features[feature_cols].isnull().mean() == 1.0
    cols_to_drop = missing_mask[missing_mask].index.tolist()
    df_features = df_features.drop(columns=cols_to_drop)
    feature_cols = [c for c in feature_cols if c not in cols_to_drop]
    
    nunique = df_features[feature_cols].nunique(dropna=True)
    cols_to_drop = nunique[nunique <= 1].index.tolist()
    df_features = df_features.drop(columns=cols_to_drop)
    feature_cols = [c for c in feature_cols if c not in cols_to_drop]
    
    df_features = df_features.dropna(subset=['TARGET'])
    return df_features, feature_cols

# =====================================================================
# 3. BENCHMARK EXECUTION
# =====================================================================

def build_model(model_name, input_dim, params, output_dim):
    if model_name == 'LSTM':
        return LSTM(input_dim, params['hidden_dim'], params['num_layers'], output_dim, params['dropout'])
    elif model_name == 'BiLSTM':
        return BiLSTM(input_dim, params['hidden_dim'], params['num_layers'], output_dim, params['dropout'])
    elif model_name == 'GRU':
        return GRU(input_dim, params['hidden_dim'], params['num_layers'], output_dim, params['dropout'])
    elif model_name == 'TCN':
        return TCN(input_dim, params['hidden_dim'], params['num_layers'], output_dim, kernel_size=2, dropout=params['dropout'])
    elif model_name == 'CNN-LSTM':
        return CNN_LSTM(input_dim, params['hidden_dim'], params['num_layers'], output_dim, kernel_size=2, dropout=params['dropout'])
    elif model_name == 'Transformer':
        return TransformerEncoderModel(input_dim, params['hidden_dim'], params['num_layers'], output_dim, nhead=4, dropout=params['dropout'])
    elif model_name == 'TemporalTransformer':
        return TemporalTransformerModel(input_dim, params['hidden_dim'], params['num_layers'], output_dim, nhead=4, dropout=params['dropout'])

def run_benchmark():
    input_dir = "/kaggle/input"
    fs_path = None
    for root, dirs, files in os.walk(input_dir):
        if "master_features.parquet" in files:
            fs_path = os.path.join(root, "master_features.parquet")
            break
            
    if not fs_path:
        print("WARNING: /kaggle/input not found, attempting local path for testing.")
        fs_path = "data/feature_store/feature_store_v1/master_features.parquet"
        
    df, feature_cols = build_temporal_dataset(fs_path)
    
    pat_df = df.groupby('PATNO').last().reset_index()
    X_pat_all = pat_df['PATNO'].values
    y_pat_all = pat_df['TARGET'].values
    
    if TASK_TYPE == "classification":
        y_binned_all = y_pat_all.astype(int)
        output_dim = 4
        criterion = nn.CrossEntropyLoss()
    else:
        bins = np.percentile(y_pat_all, [0, 25, 50, 75, 100])
        bins[-1] += 1
        y_binned_all = np.digitize(y_pat_all, bins)
        output_dim = 1
        criterion = nn.MSELoss()
    
    from sklearn.model_selection import train_test_split
    X_cv, X_tune, y_cv_binned, y_tune_binned = train_test_split(
        X_pat_all, y_binned_all, test_size=0.2, stratify=y_binned_all, random_state=42
    )
    
    X_tune_train, X_tune_val = train_test_split(X_tune, test_size=0.2, stratify=y_tune_binned, random_state=42)
    
    df_opt_train = df[df['PATNO'].isin(X_tune_train)].copy()
    df_opt_val = df[df['PATNO'].isin(X_tune_val)].copy()
    
    imputer_opt = SimpleImputer(strategy='median')
    scaler_opt = StandardScaler()
    df_opt_train[feature_cols] = scaler_opt.fit_transform(imputer_opt.fit_transform(df_opt_train[feature_cols].values))
    df_opt_val[feature_cols] = scaler_opt.transform(imputer_opt.transform(df_opt_val[feature_cols].values))
    
    def build_seqs(sub_df):
        seqs, targs = [], []
        for patno, group in sub_df.groupby('PATNO'):
            seqs.append(torch.tensor(group[feature_cols].values, dtype=torch.float32))
            if TASK_TYPE == 'classification':
                targs.append(group['TARGET'].values[-1])
            else:
                targs.append(group['TARGET'].values[-1])
        return seqs, targs
        
    opt_train_seqs, opt_train_targets = build_seqs(df_opt_train)
    opt_val_seqs, opt_val_targets = build_seqs(df_opt_val)
    
    opt_train_loader = DataLoader(SeqDataset(opt_train_seqs, opt_train_targets), batch_size=32, shuffle=True, collate_fn=collate_fn)
    opt_val_loader = DataLoader(SeqDataset(opt_val_seqs, opt_val_targets), batch_size=32, shuffle=False, collate_fn=collate_fn)
    
    cv = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=42)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device} | Task: {TASK_TYPE}")
    
    models_to_test = ['LSTM', 'BiLSTM', 'GRU', 'TCN', 'CNN-LSTM', 'Transformer', 'TemporalTransformer']
    results = []
    
    for model_name in models_to_test:
        print(f"\n{'='*50}\nEvaluating {model_name}\n{'='*50}")
        print(f"--- Running Optuna HPO (Strictly Disjoint Tuning Pool) ---")
        
        def objective(trial):
            hidden_dim = trial.suggest_categorical('hidden_dim', [32, 64, 128])
            params = {
                'hidden_dim': hidden_dim,
                'num_layers': trial.suggest_int('num_layers', 1, 3),
                'dropout': trial.suggest_float('dropout', 0.1, 0.5),
                'lr': trial.suggest_float('lr', 1e-4, 5e-3, log=True)
            }
            
            model = build_model(model_name, len(feature_cols), params, output_dim).to(device)
            optimizer = torch.optim.Adam(model.parameters(), lr=params['lr'], weight_decay=1e-5)
            
            best_val_loss = float('inf')
            for ep in range(15): 
                model.train()
                for bx, by, lens in opt_train_loader:
                    bx, by, lens = bx.to(device), by.to(device), lens.to(device)
                    optimizer.zero_grad()
                    out = model(bx, lens)
                    if TASK_TYPE == 'regression': out = out.squeeze()
                    loss = criterion(out, by)
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    optimizer.step()
                    
                model.eval()
                val_loss = 0
                with torch.no_grad():
                    for bx, by, lens in opt_val_loader:
                        bx, by, lens = bx.to(device), by.to(device), lens.to(device)
                        out = model(bx, lens)
                        if TASK_TYPE == 'regression': out = out.squeeze()
                        val_loss += criterion(out, by).item()
                best_val_loss = min(best_val_loss, val_loss / len(opt_val_loader))
            return best_val_loss
            
        study = optuna.create_study(direction='minimize')
        study.optimize(objective, n_trials=10)
        best_params = study.best_params
        print(f"Best params for {model_name}: {best_params}")
        
        fold_metrics = []
        for fold, (train_idx, val_idx) in enumerate(cv.split(X_cv, y_cv_binned, groups=X_cv)):
            print(f"--- FOLD {fold+1}/5 ---")
            train_pats = X_cv[train_idx]
            val_pats = X_cv[val_idx]
            
            df_train = df[df['PATNO'].isin(train_pats)].copy()
            df_val = df[df['PATNO'].isin(val_pats)].copy()
            
            imputer = SimpleImputer(strategy='median')
            scaler = StandardScaler()
            df_train[feature_cols] = scaler.fit_transform(imputer.fit_transform(df_train[feature_cols].values))
            df_val[feature_cols] = scaler.transform(imputer.transform(df_val[feature_cols].values))
            
            train_seqs, train_targets = build_seqs(df_train)
            val_seqs, val_targets = build_seqs(df_val)
            
            full_train_loader = DataLoader(SeqDataset(train_seqs, train_targets), batch_size=32, shuffle=True, collate_fn=collate_fn)
            val_loader = DataLoader(SeqDataset(val_seqs, val_targets), batch_size=32, shuffle=False, collate_fn=collate_fn)
            
            model = build_model(model_name, len(feature_cols), best_params, output_dim).to(device)
            optimizer = torch.optim.Adam(model.parameters(), lr=best_params['lr'], weight_decay=1e-5)
            
            for ep in range(25): 
                model.train()
                for bx, by, lens in full_train_loader:
                    bx, by, lens = bx.to(device), by.to(device), lens.to(device)
                    optimizer.zero_grad()
                    out = model(bx, lens)
                    if TASK_TYPE == 'regression': out = out.squeeze()
                    loss = criterion(out, by)
                    loss.backward()
                    torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                    optimizer.step()
            
            model.eval()
            val_preds, val_trues = [], []
            with torch.no_grad():
                for bx, by, lens in val_loader:
                    bx, by, lens = bx.to(device), by.to(device), lens.to(device)
                    out = model(bx, lens)
                    if TASK_TYPE == 'regression': 
                        val_preds.extend(out.squeeze().cpu().numpy())
                    else:
                        val_preds.extend(torch.argmax(out, dim=1).cpu().numpy())
                    val_trues.extend(by.cpu().numpy())
                    
            if TASK_TYPE == 'regression':
                rmse = np.sqrt(mean_squared_error(val_trues, val_preds))
                r2 = r2_score(val_trues, val_preds)
                fold_metrics.append({'rmse': rmse, 'r2': r2})
                print(f"Fold {fold+1} Test | RMSE: {rmse:.4f} | R2: {r2:.4f}")
            else:
                acc = accuracy_score(val_trues, val_preds)
                f1 = f1_score(val_trues, val_preds, average='macro')
                fold_metrics.append({'acc': acc, 'f1_macro': f1})
                print(f"Fold {fold+1} Test | Acc: {acc:.4f} | F1 Macro: {f1:.4f}")
            
        if TASK_TYPE == 'regression':
            mean_rmse = np.mean([m['rmse'] for m in fold_metrics])
            mean_r2 = np.mean([m['r2'] for m in fold_metrics])
            print(f"--- {model_name} FINAL CV: RMSE = {mean_rmse:.4f}, R2 = {mean_r2:.4f} ---")
            if mean_r2 > 0.80 or mean_rmse < 5.0:
                print(f"🚨 ANOMALY: {model_name} R2 is suspiciously high ({mean_r2:.4f}). Potential leakage.")
            elif mean_r2 < -0.05:
                print(f"🚨 ANOMALY: {model_name} R2 is severely negative ({mean_r2:.4f}). Catastrophic collapse.")
            results.append({'Model': model_name, 'rmse': mean_rmse, 'r2': mean_r2})
        else:
            mean_acc = np.mean([m['acc'] for m in fold_metrics])
            mean_f1 = np.mean([m['f1_macro'] for m in fold_metrics])
            print(f"--- {model_name} FINAL CV: Acc = {mean_acc:.4f}, F1 Macro = {mean_f1:.4f} ---")
            if mean_acc > 0.90 or mean_f1 > 0.90:
                print(f"🚨 ANOMALY: {model_name} F1 is suspiciously high ({mean_f1:.4f}). Potential leakage.")
            results.append({'Model': model_name, 'acc_mean': mean_acc, 'f1_macro_mean': mean_f1})
        
    print("\n====================================")
    print("  TIER 3 TEMPORAL DL LEADERBOARD")
    print("====================================")
    if TASK_TYPE == 'regression':
        res_df = pd.DataFrame(results).sort_values('rmse', ascending=True).reset_index(drop=True)
    else:
        res_df = pd.DataFrame(results).sort_values('f1_macro_mean', ascending=False).reset_index(drop=True)
    print(res_df.to_markdown())

if __name__ == "__main__":
    run_benchmark()
