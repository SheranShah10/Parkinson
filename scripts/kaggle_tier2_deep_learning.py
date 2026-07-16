"""
Tier 2: Tabular Deep Learning Benchmarks (Toggleable)
Models: FT-Transformer, TabNet, SAINT, WideDeep
"""

import os
os.system("pip install torch scikit-learn optuna -q")

import os
import time
import math
import warnings
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedGroupKFold, GroupKFold
from sklearn.metrics import f1_score, accuracy_score, balanced_accuracy_score, r2_score, mean_absolute_error, mean_squared_error
import optuna

warnings.filterwarnings('ignore')
SEED = 42

# --- 1. DATA LOADING & PURGE ---
def collapse_nhy(raw_values):
    mapped = np.full(raw_values.shape, np.nan)
    valid = ~np.isnan(raw_values)
    v = raw_values[valid]
    out = np.select([v == 0, v == 1, v == 2, v >= 3], [0, 1, 2, 3], default=np.nan)
    mapped[valid] = out
    return mapped

def get_clean_data(task_type="classification"):
    input_dir = "/kaggle/input"
    fs_path = None
    for root, dirs, files in os.walk(input_dir):
        if "master_features.parquet" in files:
            fs_path = os.path.join(root, "master_features.parquet")
            break
    if not fs_path:
        fs_path = "data/feature_store/feature_store_v1/master_features.parquet"
        if not os.path.exists(fs_path):
            raise FileNotFoundError("master_features.parquet not found.")

    df = pd.read_parquet(fs_path)
    
    if task_type == "classification":
        y_raw = collapse_nhy(df['NHY'].values.astype(float))
    else:
        y_raw = df['NP3TOT'].values

    groups = df['PATNO'].values
    
    valid_idx = ~np.isnan(y_raw)
    df_valid = df.iloc[valid_idx].copy()
    y = y_raw[valid_idx]
    if task_type == "classification":
        y = y.astype(int)
    groups = groups[valid_idx]

    leaky_patterns = ['NHY', 'NP3', 'TARGET_', 'MOTOR_SEVERITY', 'TEMPORAL_MOTOR_SLOPE', 'PD_DX', 'CLINI_', 'MDS-U_'] 
    leaky_cols = [c for c in df_valid.columns if any(pat in c.upper() for pat in leaky_patterns)]
    df_features = df_valid.drop(columns=leaky_cols + ['PATNO', 'EVENT_ID'], errors='ignore')

    missing_mask = df_features.isnull().mean() == 1.0
    df_features = df_features.loc[:, ~missing_mask]
    
    nunique = df_features.nunique(dropna=True)
    df_features = df_features.drop(columns=nunique[nunique <= 1].index.tolist())
    
    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    X = df_features[numeric_cols].values
    
    return X, y, groups, numeric_cols.tolist()

# --- 2. ARCHITECTURES ---

class FeatureTokenizer(nn.Module):
    def __init__(self, num_numerical, d_token):
        super().__init__()
        self.weight = nn.Parameter(torch.Tensor(num_numerical, d_token))
        self.bias = nn.Parameter(torch.Tensor(num_numerical, d_token))
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        nn.init.zeros_(self.bias)

    def forward(self, x):
        return x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)

class FTTransformer(nn.Module):
    def __init__(self, input_dim, d_token, n_blocks, num_heads, output_dim, dropout=0.2):
        super().__init__()
        self.tokenizer = FeatureTokenizer(input_dim, d_token)
        self.cls_token = nn.Parameter(torch.Tensor(1, 1, d_token))
        nn.init.kaiming_uniform_(self.cls_token, a=math.sqrt(5))
        encoder_layer = nn.TransformerEncoderLayer(d_model=d_token, nhead=num_heads, dim_feedforward=d_token * 2, dropout=dropout, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_blocks)
        self.head = nn.Sequential(nn.LayerNorm(d_token), nn.ReLU(), nn.Linear(d_token, output_dim))

    def forward(self, x):
        B = x.size(0)
        x = self.tokenizer(x)
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)
        x = self.transformer(x)
        return self.head(x[:, 0, :])

class Sparsemax(nn.Module):
    def __init__(self, dim=-1):
        super(Sparsemax, self).__init__()
        self.dim = dim

    def forward(self, input):
        original_size = input.size()
        input = input.view(-1, input.size(self.dim))
        dim = 1
        number_of_logits = input.size(dim)
        zs = torch.sort(input, dim=dim, descending=True)[0]
        range_v = torch.arange(1, number_of_logits + 1, dtype=input.dtype, device=input.device).view(1, -1)
        bound = 1 + range_v * zs
        cumulative_sum_zs = torch.cumsum(zs, dim)
        is_gt = bound > cumulative_sum_zs
        k = torch.max(is_gt * range_v, dim, keepdim=True)[0]
        tau = (torch.gather(cumulative_sum_zs, dim, (k - 1).long()) - 1) / k
        output = torch.clamp(input - tau, min=0)
        return output.view(original_size)

class TabNetWrapper(nn.Module):
    def __init__(self, input_dim, n_d=16, n_a=16, n_steps=3, gamma=1.3, output_dim=2):
        super().__init__()
        self.n_d = n_d
        self.n_a = n_a
        self.n_steps = n_steps
        self.gamma = gamma
        self.initial_bn = nn.BatchNorm1d(input_dim)
        
        self.feature_transformers = nn.ModuleList([
            nn.Sequential(nn.Linear(input_dim, (n_d + n_a) * 2), nn.BatchNorm1d((n_d + n_a) * 2), nn.GLU(dim=-1)) for _ in range(n_steps)
        ])
        self.attentive_transformers = nn.ModuleList([
            nn.Sequential(nn.Linear(n_a, input_dim), nn.BatchNorm1d(input_dim), Sparsemax(dim=-1)) for _ in range(n_steps)
        ])
        self.final_mapping = nn.Linear(n_d, output_dim)
        
    def forward(self, x):
        x = self.initial_bn(x)
        prior_scales = torch.ones_like(x)
        out_accumulator = 0
        a_prev = torch.zeros(x.size(0), self.n_a, device=x.device)
        for step in range(self.n_steps):
            mask = self.attentive_transformers[step](a_prev) if step > 0 else prior_scales
            prior_scales = prior_scales * (self.gamma - mask)
            ft_out = self.feature_transformers[step](x * mask)
            d = ft_out[:, :self.n_d]
            a_prev = ft_out[:, self.n_d:]
            out_accumulator = out_accumulator + d
        return self.final_mapping(out_accumulator)

class SAINTBlock(nn.Module):
    def __init__(self, d_model, num_heads, dropout):
        super().__init__()
        self.feature_attention = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.intersample_attention = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.ffn = nn.Sequential(nn.Linear(d_model, d_model * 2), nn.ReLU(), nn.Dropout(dropout), nn.Linear(d_model * 2, d_model))
        self.ln1 = nn.LayerNorm(d_model)
        self.ln2 = nn.LayerNorm(d_model)
        self.ln3 = nn.LayerNorm(d_model)

    def forward(self, x):
        x_norm = self.ln1(x)
        attn_out, _ = self.feature_attention(x_norm, x_norm, x_norm)
        x = x + attn_out
        x_norm = self.ln2(x)
        x_norm_t = x_norm.transpose(0, 1)
        attn_out_t, _ = self.intersample_attention(x_norm_t, x_norm_t, x_norm_t)
        x = x + attn_out_t.transpose(0, 1)
        x = x + self.ffn(self.ln3(x))
        return x

class SAINT(nn.Module):
    def __init__(self, input_dim, d_model, num_heads, num_blocks, output_dim, dropout=0.2):
        super().__init__()
        self.tokenizer = nn.Parameter(torch.randn(input_dim, d_model))
        self.cls_token = nn.Parameter(torch.randn(1, 1, d_model))
        self.blocks = nn.ModuleList([SAINTBlock(d_model, num_heads, dropout) for _ in range(num_blocks)])
        self.head = nn.Linear(d_model, output_dim)

    def forward(self, x):
        B = x.size(0)
        x_emb = x.unsqueeze(-1) * self.tokenizer.unsqueeze(0)
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x_emb = torch.cat((cls_tokens, x_emb), dim=1)
        for block in self.blocks: x_emb = block(x_emb)
        return self.head(x_emb[:, 0, :])

class WideDeep(nn.Module):
    def __init__(self, input_dim, deep_hidden_dims, output_dim, dropout=0.3):
        super().__init__()
        self.wide = nn.Linear(input_dim, output_dim)
        layers = []
        in_d = input_dim
        for h in deep_hidden_dims:
            layers.extend([nn.Linear(in_d, h), nn.BatchNorm1d(h), nn.ReLU(), nn.Dropout(dropout)])
            in_d = h
        layers.append(nn.Linear(in_d, output_dim))
        self.deep = nn.Sequential(*layers)
        
    def forward(self, x):
        return self.wide(x) + self.deep(x)

# --- 3. TRAINER ---
class Trainer:
    def __init__(self, model, optimizer, criterion, device, is_regression):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.criterion = criterion
        self.device = device
        self.is_regression = is_regression

    def train_epoch(self, dataloader):
        self.model.train()
        total_loss = 0
        for X, y in dataloader:
            X, y = X.to(self.device), y.to(self.device)
            if self.is_regression:
                y = y.unsqueeze(1).float()
            self.optimizer.zero_grad()
            outputs = self.model(X)
            loss = self.criterion(outputs, y)
            loss.backward()
            self.optimizer.step()
            total_loss += loss.item()
        return total_loss / len(dataloader)

    def validate_epoch(self, dataloader):
        self.model.eval()
        total_loss = 0
        all_preds, all_targets = [], []
        with torch.no_grad():
            for X, y in dataloader:
                X, y = X.to(self.device), y.to(self.device)
                if self.is_regression:
                    y = y.unsqueeze(1).float()
                outputs = self.model(X)
                loss = self.criterion(outputs, y)
                total_loss += loss.item()
                
                if self.is_regression:
                    all_preds.extend(outputs.cpu().numpy())
                    all_targets.extend(y.cpu().numpy())
                else:
                    preds = torch.argmax(outputs, dim=1)
                    all_preds.extend(preds.cpu().numpy())
                    all_targets.extend(y.cpu().numpy())
                    
        avg_loss = total_loss / len(dataloader)
        if self.is_regression:
            metrics = {
                'rmse': np.sqrt(mean_squared_error(all_targets, all_preds)),
                'r2': r2_score(all_targets, all_preds)
            }
        else:
            metrics = {
                'f1_macro': f1_score(all_targets, all_preds, average='macro'),
                'acc': accuracy_score(all_targets, all_preds)
            }
        return avg_loss, metrics

# --- 4. ORCHESTRATION ---
def build_model(trial, model_name, input_dim, output_dim):
    dropout = trial.suggest_float("dropout", 0.1, 0.4)
    if model_name == "FTTransformer":
        d_token = trial.suggest_categorical("d_token", [32, 64])
        n_blocks = trial.suggest_int("n_blocks", 1, 3)
        return FTTransformer(input_dim, d_token, n_blocks, 4, output_dim, dropout)
    elif model_name == "TabNet":
        n_d = trial.suggest_categorical("n_d", [16, 32])
        n_steps = trial.suggest_int("n_steps", 2, 4)
        return TabNetWrapper(input_dim, n_d, n_d, n_steps, 1.3, output_dim)
    elif model_name == "SAINT":
        d_model = trial.suggest_categorical("d_model", [32, 64])
        n_blocks = trial.suggest_int("n_blocks", 1, 2)
        return SAINT(input_dim, d_model, 4, n_blocks, output_dim, dropout)
    elif model_name == "WideDeep":
        hidden = trial.suggest_categorical("hidden_dims", [[128, 64], [256, 128, 64]])
        return WideDeep(input_dim, hidden, output_dim, dropout)

def run_benchmark(task_type="classification", n_trials=10, epochs=10):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device} | Task: {task_type.upper()}")
    
    X, y, groups, _ = get_clean_data(task_type)
    output_dim = 4 if task_type == "classification" else 1
    is_reg = task_type == "regression"
    
    print(f"Data Loaded: {X.shape[0]} rows, {X.shape[1]} features.")

    results = []
    models_to_test = ["WideDeep", "FTTransformer", "TabNet", "SAINT"]
    
    # 5-Fold Cross Validation Loop
    cv = GroupKFold(n_splits=5) if is_reg else StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    
    for model_name in models_to_test:
        print(f"\n====================================")
        print(f" EVALUATING: {model_name}")
        print(f"====================================")
        
        fold_metrics = []
        for fold, (train_idx, val_idx) in enumerate(cv.split(X, y, groups), 1):
            print(f"  --- Fold {fold} ---")
            
            imputer = SimpleImputer(strategy='median')
            scaler = StandardScaler()
            X_train = scaler.fit_transform(imputer.fit_transform(X[train_idx]))
            X_val = scaler.transform(imputer.transform(X[val_idx]))
            
            X_t_train = torch.tensor(X_train, dtype=torch.float32)
            y_t_train = torch.tensor(y[train_idx], dtype=torch.float32 if is_reg else torch.long)
            X_t_val = torch.tensor(X_val, dtype=torch.float32)
            y_t_val = torch.tensor(y[val_idx], dtype=torch.float32 if is_reg else torch.long)
            
            def objective(trial):
                lr = trial.suggest_float("lr", 1e-4, 5e-3, log=True)
                batch_size = trial.suggest_categorical("batch_size", [64, 128])
                model = build_model(trial, model_name, X_train.shape[1], output_dim)
                optimizer = optim.Adam(model.parameters(), lr=lr)
                criterion = nn.MSELoss() if is_reg else nn.CrossEntropyLoss()
                
                trainer = Trainer(model, optimizer, criterion, device, is_reg)
                train_loader = DataLoader(TensorDataset(X_t_train, y_t_train), batch_size=batch_size, shuffle=True)
                val_loader = DataLoader(TensorDataset(X_t_val, y_t_val), batch_size=batch_size, shuffle=False)
                
                best_val_loss = float('inf')
                for epoch in range(epochs):
                    trainer.train_epoch(train_loader)
                    val_loss, _ = trainer.validate_epoch(val_loader)
                    if val_loss < best_val_loss: best_val_loss = val_loss
                
                # ANOMALY FLAG (Smoke Test Equivalent)
                if is_reg and best_val_loss < 2.0:
                    raise ValueError(f"🚨 ANOMALY: {model_name} Regression MSE {best_val_loss:.2f} is impossibly low (leak!).")
                if not is_reg and best_val_loss < 0.15:
                    raise ValueError(f"🚨 ANOMALY: {model_name} Classification Loss {best_val_loss:.4f} is impossibly low (leak!).")
                    
                return best_val_loss

            study = optuna.create_study(direction="minimize")
            study.optimize(objective, n_trials=n_trials, show_progress_bar=False)
            
            best_model = build_model(study.best_trial, model_name, X_train.shape[1], output_dim)
            optimizer = optim.Adam(best_model.parameters(), lr=study.best_trial.params['lr'])
            criterion = nn.MSELoss() if is_reg else nn.CrossEntropyLoss()
            trainer = Trainer(best_model, optimizer, criterion, device, is_reg)
            
            train_loader = DataLoader(TensorDataset(X_t_train, y_t_train), batch_size=study.best_trial.params['batch_size'], shuffle=True)
            val_loader = DataLoader(TensorDataset(X_t_val, y_t_val), batch_size=study.best_trial.params['batch_size'], shuffle=False)
            
            for epoch in range(epochs + 5):
                trainer.train_epoch(train_loader)
            _, final_metrics = trainer.validate_epoch(val_loader)
            fold_metrics.append(final_metrics)
            print(f"      Best Val Loss: {study.best_value:.4f} | Metrics: {final_metrics}")
            
        mean_metrics = {k: np.mean([f[k] for f in fold_metrics]) for k in fold_metrics[0].keys()}
        results.append({"Model": model_name, **mean_metrics})
        
    print("\n====================================")
    print(f" {task_type.upper()} LEADERBOARD")
    print("====================================")
    print(pd.DataFrame(results).to_markdown(index=False))

if __name__ == "__main__":
    # TOGGLEABLE EXECUTION
    # Set to True to run classification, False to skip
    RUN_CLASSIFICATION = True
    
    # Set to True to run regression, False to skip
    RUN_REGRESSION = False
    
    N_TRIALS = 10
    EPOCHS = 10
    
    if RUN_CLASSIFICATION:
        run_benchmark("classification", n_trials=N_TRIALS, epochs=EPOCHS)
        
    if RUN_REGRESSION:
        run_benchmark("regression", n_trials=N_TRIALS, epochs=EPOCHS)
