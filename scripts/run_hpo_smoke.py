import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
import optuna

# ---------------------------------------------------------
# 1. VERIFIED MODEL & TRAINER CLASSES
# ---------------------------------------------------------
class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim, dropout=0.3):
        super().__init__()
        layers = []
        in_d = input_dim
        for h in hidden_dims:
            layers.extend([nn.Linear(in_d, h), nn.BatchNorm1d(h), nn.ReLU(), nn.Dropout(dropout)])
            in_d = h
        layers.append(nn.Linear(in_d, output_dim))
        self.network = nn.Sequential(*layers)
        
    def forward(self, x): 
        return self.network(x)

class Trainer:
    def __init__(self, model, optimizer, scheduler, criterion, device, checkpoint_dir):
        self.model = model.to(device)
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion
        self.device = device
        self.scaler = torch.amp.GradScaler('cuda') if torch.cuda.is_available() else None
        self.checkpoint_dir = checkpoint_dir

    def train_epoch(self, dataloader):
        self.model.train()
        total_loss = 0
        for X, y in dataloader:
            X, y = X.to(self.device), y.to(self.device)
            self.optimizer.zero_grad()
            if self.scaler:
                with torch.amp.autocast('cuda'):
                    outputs = self.model(X)
                    loss = self.criterion(outputs, y)
                self.scaler.scale(loss).backward()
                self.scaler.step(self.optimizer)
                self.scaler.update()
            else:
                outputs = self.model(X)
                loss = self.criterion(outputs, y)
                loss.backward()
                self.optimizer.step()
            total_loss += loss.item()
        return total_loss / len(dataloader)

    def validate_epoch(self, dataloader):
        self.model.eval()
        total_loss = 0
        with torch.no_grad():
            for X, y in dataloader:
                X, y = X.to(self.device), y.to(self.device)
                outputs = self.model(X)
                loss = self.criterion(outputs, y)
                total_loss += loss.item()
        return total_loss / len(dataloader)

# ---------------------------------------------------------
# 2. HPO OBJECTIVE & ORCHESTRATION
# ---------------------------------------------------------
def run_hpo_smoke():
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device acquired: {device}\n")
    
    # LOAD DATA
    input_dir = "/kaggle/input"
    fs_path = None
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file == "master_features.parquet":
                fs_path = os.path.join(root, file)
                break
                
    if fs_path:
        df = pd.read_parquet(fs_path)
    else:
        print("Dataset not found. Aborting.")
        return
        
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    raw_values = df[numeric_cols].values
    
    imputer = SimpleImputer(strategy='median')
    scaler = StandardScaler()
    processed_values = scaler.fit_transform(imputer.fit_transform(raw_values))
    
    # Verified target from Phase 8.1 smoke test
    median_val = np.median(processed_values[:, 0])
    y_full = (processed_values[:, 0] > median_val).astype(int)
    
    # EXTRACT PATIENT IDS FOR ZERO-LEAKAGE SPLITTING
    # Phase 6 data natively contains PATNO
    groups = df['PATNO'].values
    
    # ---------------------------------------------------------
    # ZERO-LEAKAGE VALIDATION SPLIT
    # ---------------------------------------------------------
    gkf = GroupKFold(n_splits=5)
    train_idx, val_idx = next(gkf.split(processed_values, y_full, groups))
    
    X_train_t = torch.tensor(processed_values[train_idx], dtype=torch.float32)
    y_train_t = torch.tensor(y_full[train_idx], dtype=torch.long)
    
    X_val_t = torch.tensor(processed_values[val_idx], dtype=torch.float32)
    y_val_t = torch.tensor(y_full[val_idx], dtype=torch.long)
    
    print(f"Zero-Leakage Split Achieved!")
    print(f"Train Size: {len(X_train_t)} (Patients kept perfectly isolated)")
    print(f"Val Size:   {len(X_val_t)}")
    
    # OPTUNA OBJECTIVE FUNCTION
    def objective(trial):
        # SEARCH SPACE
        lr = trial.suggest_float("lr", 1e-5, 1e-2, log=True)
        batch_size = trial.suggest_categorical("batch_size", [16, 32, 64, 128])
        dropout = trial.suggest_float("dropout", 0.1, 0.5)
        
        hidden_variants = [[64, 32], [128, 64], [256, 128, 64]]
        hidden_idx = trial.suggest_categorical("hidden_idx", [0, 1, 2])
        hidden_dims = hidden_variants[hidden_idx]
        
        train_dataset = TensorDataset(X_train_t, y_train_t)
        val_dataset = TensorDataset(X_val_t, y_val_t)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
        
        model = MLP(input_dim=X_train_t.shape[1], hidden_dims=hidden_dims, output_dim=2, dropout=dropout)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=lr)
        
        trainer = Trainer(model, optimizer, None, criterion, device, "/kaggle/working/")
        
        # Train for 3 epochs per trial
        for epoch in range(3):
            trainer.train_epoch(train_loader)
            
        # SCORE ON STRICT VALIDATION SET
        val_loss = trainer.validate_epoch(val_loader)
        return val_loss

    # ---------------------------------------------------------
    # EXECUTE SMOKE STUDY (5-10 TRIALS)
    # ---------------------------------------------------------
    print("\n--- INITIATING OPTUNA SMOKE STUDY (10 TRIALS) ---")
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=10)
    
    print("\n--- SMOKE STUDY COMPLETE ---")
    print(f"Best Validation Loss Achieved: {study.best_value:.4f}")
    print("Best Hyperparameters:")
    for key, value in study.best_params.items():
        print(f"    {key}: {value}")
        
    print("\nVariation Output Check: Look at the 10 trials above. Did Validation Loss vary dynamically between trials?")

if __name__ == "__main__":
    run_hpo_smoke()
