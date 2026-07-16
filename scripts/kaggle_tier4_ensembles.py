import os
import gc
import warnings
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torch.nn.utils.rnn import pad_sequence, pack_padded_sequence, pad_packed_sequence
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, f1_score
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from catboost import CatBoostRegressor, CatBoostClassifier

warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURATION & HARDCODED VERIFIED HYPERPARAMETERS
# ==============================================================================
TASK_TYPE = 'regression'  # Change to 'classification' to run the classification ensemble

TARGET_REG = 'NP3TOT'
TARGET_CLF = 'TARGET'
N_SPLITS = 5
RANDOM_STATE = 42
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# CatBoost & GBDT Params (From Tier 1, un-tuned defaults with Seed 42)
CATBOOST_PARAMS = {'verbose': 0, 'thread_count': -1, 'random_state': RANDOM_STATE}
GB_PARAMS = {'random_state': RANDOM_STATE}

# GRU Params (Exact best_params from Tier 3 Optuna Logs)
GRU_PARAMS = {
    'hidden_dim': 128, 
    'num_layers': 2, 
    'dropout': 0.229075213006653, 
    'lr': 0.002415226090863938
}

# ==============================================================================
# EXACT VERIFIED TIER 3 DATA PIPELINE (Copied from kaggle_tier3_temporal_dl.py)
# ==============================================================================

def build_temporal_dataset(df_path):
    print(f"Loading data from: {df_path}")
    df = pd.read_parquet(df_path)
    
    event_order = {'BL':0, 'V01':1, 'V02':2, 'V03':3, 'V04':4, 'V05':5, 'V06':6, 'V07':7, 'V08':8, 'V09':9, 
                   'V10':10, 'V11':11, 'V12':12, 'V13':13, 'V14':14, 'V15':15, 'V16':16, 'V17':17, 'V18':18}
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

def build_seqs(sub_df, feature_cols):
    seqs, targs = [], []
    for patno, group in sub_df.groupby('PATNO'):
        seqs.append(torch.tensor(group[feature_cols].values, dtype=torch.float32))
        targs.append(group['TARGET'].values[-1])
    return seqs, targs

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
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1).to(out.device)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
        return self.fc(last_out)

# ==============================================================================
# ENSEMBLE PIPELINE
# ==============================================================================

def run_ensembles():
    print(f"--- STARTING TIER 4 ENSEMBLES ({TASK_TYPE.upper()}) ---")
    
    # Use Kaggle path if available
    input_dir = "/kaggle/input"
    parquet_path = None
    for root, dirs, files in os.walk(input_dir):
        if "master_features.parquet" in files:
            parquet_path = os.path.join(root, "master_features.parquet")
            break
    if not parquet_path:
        parquet_path = "data/feature_store/feature_store_v1/master_features.parquet"

    print("Executing Verified Tier 3 Purge and Builder...")
    df_features, feature_cols = build_temporal_dataset(parquet_path)
    
    # Build Aligned Tabular Dataset (Using the LAST visit of the exact same sequence)
    print("Building Synchronized Tabular Data...")
    df_tab = df_features.groupby('PATNO').last().reset_index()
    X_tab = df_tab[feature_cols].values.astype(np.float32)
    y_aligned = df_tab['TARGET'].values
    groups_aligned = df_tab['PATNO'].values
    
    print(f"Verified Patient Count: {len(y_aligned)}")
    print(f"Verified Tabular Feature Count: {len(feature_cols)}")
    
    # Prepare OOF Storage
    num_samples = len(y_aligned)
    if TASK_TYPE == 'regression':
        oof_gbdt = np.zeros(num_samples)
        oof_cat = np.zeros(num_samples)
        oof_rnn = np.zeros(num_samples)
    else:
        oof_gbdt = np.zeros((num_samples, 4))
        oof_cat = np.zeros((num_samples, 4))
        oof_rnn = np.zeros((num_samples, 4))

    cv = StratifiedGroupKFold(n_splits=N_SPLITS, shuffle=True, random_state=RANDOM_STATE)
    
    for fold, (train_idx, val_idx) in enumerate(cv.split(X_tab, y_aligned, groups_aligned)):
        print(f"\n--- FOLD {fold+1}/{N_SPLITS} ---")
        
        train_pats = groups_aligned[train_idx]
        val_pats = groups_aligned[val_idx]
        
        # 1. Prepare Tabular
        X_tab_train, y_train = X_tab[train_idx], y_aligned[train_idx]
        X_tab_val, y_val = X_tab[val_idx], y_aligned[val_idx]
        
        # 2. Prepare Sequential (Strict Tier 3 replication)
        df_train = df_features[df_features['PATNO'].isin(train_pats)].copy()
        df_val = df_features[df_features['PATNO'].isin(val_pats)].copy()
        
        imputer = SimpleImputer(strategy='median')
        scaler = StandardScaler()
        
        df_train[feature_cols] = scaler.fit_transform(imputer.fit_transform(df_train[feature_cols].values))
        df_val[feature_cols] = scaler.transform(imputer.transform(df_val[feature_cols].values))
        
        # Build strict sequences
        train_seqs, train_targets = build_seqs(df_train, feature_cols)
        val_seqs, val_targets = build_seqs(df_val, feature_cols)
        
        train_loader = DataLoader(SeqDataset(train_seqs, train_targets), batch_size=32, shuffle=True, collate_fn=collate_fn)
        val_loader = DataLoader(SeqDataset(val_seqs, val_targets), batch_size=32, shuffle=False, collate_fn=collate_fn)
        
        # --- Train Tier 1 Models ---
        print("Training Tier 1 (GBDT & CatBoost)...")
        if TASK_TYPE == 'regression':
            model_gbdt = GradientBoostingRegressor(**GB_PARAMS)
            model_cat = CatBoostRegressor(**CATBOOST_PARAMS)
        else:
            model_gbdt = GradientBoostingClassifier(**GB_PARAMS)
            model_cat = CatBoostClassifier(**CATBOOST_PARAMS)
            
        # We must impute Tabular NaNs before fitting tree models
        X_tab_train_imp = imputer.fit_transform(X_tab_train)
        X_tab_val_imp = imputer.transform(X_tab_val)
        
        model_gbdt.fit(X_tab_train_imp, y_train)
        model_cat.fit(X_tab_train_imp, y_train)
        
        if TASK_TYPE == 'regression':
            oof_gbdt[val_idx] = model_gbdt.predict(X_tab_val_imp)
            oof_cat[val_idx] = model_cat.predict(X_tab_val_imp)
        else:
            oof_gbdt[val_idx] = model_gbdt.predict_proba(X_tab_val_imp)
            oof_cat[val_idx] = model_cat.predict_proba(X_tab_val_imp)
            
        # --- Train Tier 3 Model (GRU) ---
        print("Training Tier 3 (GRU)...")
        output_dim = 1 if TASK_TYPE == 'regression' else 4
        model_rnn = GRU(len(feature_cols), GRU_PARAMS['hidden_dim'], GRU_PARAMS['num_layers'], output_dim, GRU_PARAMS['dropout']).to(DEVICE)
        
        criterion = nn.MSELoss() if TASK_TYPE == 'regression' else nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model_rnn.parameters(), lr=GRU_PARAMS['lr'], weight_decay=1e-5)
        
        for ep in range(25): # Fixed epochs from Tier 3
            model_rnn.train()
            for bx, by, lens in train_loader:
                bx, by = bx.to(DEVICE), by.to(DEVICE)
                optimizer.zero_grad()
                out = model_rnn(bx, lens.cpu())
                if TASK_TYPE == 'regression': out = out.squeeze()
                loss = criterion(out, by)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model_rnn.parameters(), max_norm=1.0)
                optimizer.step()
                
        # RNN OOF Predict
        model_rnn.eval()
        val_preds = []
        with torch.no_grad():
            for bx, by, lens in val_loader:
                bx, by = bx.to(DEVICE), by.to(DEVICE)
                out = model_rnn(bx, lens.cpu())
                if TASK_TYPE == 'regression':
                    val_preds.extend(out.squeeze().cpu().numpy())
                else:
                    val_preds.extend(torch.softmax(out, dim=1).cpu().numpy())
        
        if TASK_TYPE == 'regression': 
            oof_rnn[val_idx] = np.array(val_preds)
        else: 
            oof_rnn[val_idx] = np.array(val_preds)

        del model_gbdt, model_cat, model_rnn; gc.collect(); torch.cuda.empty_cache()

    # ==============================================================================
    # META-MODELS & ENSEMBLING
    # ==============================================================================
    print("\n--- CALCULATING FINAL ENSEMBLES ---")
    
    if TASK_TYPE == 'regression':
        rmse_gb = np.sqrt(mean_squared_error(y_aligned, oof_gbdt))
        r2_gb = r2_score(y_aligned, oof_gbdt)
        print(f"Base GBDT    | RMSE: {rmse_gb:.4f} | R2: {r2_gb:.4f}")
        
        rmse_cat = np.sqrt(mean_squared_error(y_aligned, oof_cat))
        r2_cat = r2_score(y_aligned, oof_cat)
        print(f"Base CatBoost| RMSE: {rmse_cat:.4f} | R2: {r2_cat:.4f}")
        
        rmse_rnn = np.sqrt(mean_squared_error(y_aligned, oof_rnn))
        r2_rnn = r2_score(y_aligned, oof_rnn)
        print(f"Base GRU     | RMSE: {rmse_rnn:.4f} | R2: {r2_rnn:.4f}")
    else:
        f1_gb = f1_score(y_aligned, oof_gbdt.argmax(axis=1), average='macro')
        print(f"Base GBDT    | F1: {f1_gb:.4f}")
        
        f1_cat = f1_score(y_aligned, oof_cat.argmax(axis=1), average='macro')
        print(f"Base CatBoost| F1: {f1_cat:.4f}")
        
        f1_rnn = f1_score(y_aligned, oof_rnn.argmax(axis=1), average='macro')
        print(f"Base GRU     | F1: {f1_rnn:.4f}")

    print("\n1. Voting Ensemble (Unweighted Average)")
    oof_voting = (oof_gbdt + oof_cat + oof_rnn) / 3.0
    if TASK_TYPE == 'regression':
        rmse_vote = np.sqrt(mean_squared_error(y_aligned, oof_voting))
        r2_vote = r2_score(y_aligned, oof_voting)
        print(f"Voting Ensemble | RMSE: {rmse_vote:.4f} | R2: {r2_vote:.4f}")
    else:
        f1_vote = f1_score(y_aligned, oof_voting.argmax(axis=1), average='macro')
        print(f"Voting Ensemble | F1: {f1_vote:.4f}")

    print("\n2. Stacking Ensemble (Meta-Model)")
    if TASK_TYPE == 'regression':
        X_meta = np.column_stack([oof_gbdt, oof_cat, oof_rnn])
        meta_model = Ridge()
    else:
        X_meta = np.hstack([oof_gbdt, oof_cat, oof_rnn])
        meta_model = LogisticRegression(max_iter=1000)
    
    stack_preds = np.zeros_like(oof_gbdt)
    for train_idx, val_idx in cv.split(X_meta, y_aligned, groups_aligned):
        meta_model.fit(X_meta[train_idx], y_aligned[train_idx])
        if TASK_TYPE == 'regression':
            stack_preds[val_idx] = meta_model.predict(X_meta[val_idx])
        else:
            stack_preds[val_idx] = meta_model.predict_proba(X_meta[val_idx])

    if TASK_TYPE == 'regression':
        rmse_stack = np.sqrt(mean_squared_error(y_aligned, stack_preds))
        r2_stack = r2_score(y_aligned, stack_preds)
        print(f"Stacking Ensemble | RMSE: {rmse_stack:.4f} | R2: {r2_stack:.4f}")
    else:
        f1_stack = f1_score(y_aligned, stack_preds.argmax(axis=1), average='macro')
        print(f"Stacking Ensemble | F1: {f1_stack:.4f}")

if __name__ == "__main__":
    run_ensembles()
