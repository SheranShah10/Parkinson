import os
import sys
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np

# Ensure src is in path
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path: sys.path.insert(0, base_dir)

from src.deep_learning.models.tabular_models import MLP
from src.deep_learning.training.trainer import Trainer

print("============================================================")
print("KAGGLE SMOKE TEST (PHASE 8.1 & 8.3 END-TO-END VALIDATION)")
print("============================================================")

def run_smoke_test():
    # 1. Device check
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device acquired: {device}")
    
    # 2. Data Load (Fallback to dummy if Kaggle paths differ, but attempt Phase 6 load)
    fs_path = os.path.join(base_dir, "data", "feature_store", "feature_store_v1", "master_features.parquet")
    print(f"Loading Phase 6 data from: {fs_path}")
    
    try:
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import StandardScaler
        
        df = pd.read_parquet(fs_path)
        # Use all numeric features
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        # FIX: Handle NaNs and Unscaled Data
        raw_values = df[numeric_cols].values
        imputer = SimpleImputer(strategy='median')
        scaler = StandardScaler()
        
        processed_values = scaler.fit_transform(imputer.fit_transform(raw_values))
        
        X = torch.tensor(processed_values, dtype=torch.float32)
        # Dummy binary target for smoke test
        y = torch.tensor(np.random.randint(0, 2, size=(len(df),)), dtype=torch.long)
        print(f"Real data loaded, imputed, and scaled successfully. Shape: {X.shape}")
    except Exception as e:
        print(f"Could not load real data: {e}. Falling back to synthesized batch for smoke test.")
        X = torch.randn(10, 554)
        y = torch.randint(0, 2, (10,))
        
    dataset = TensorDataset(X, y)
    dataloader = DataLoader(dataset, batch_size=2, shuffle=True)
    
    # Update input_dim to match X.shape[1]
    model = MLP(input_dim=X.shape[1], hidden_dims=[16], output_dim=2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.01)
    
    ckpt_dir = os.path.join(base_dir, "artifacts", "deep_learning", "checkpoints")
    os.makedirs(ckpt_dir, exist_ok=True)
    
    trainer = Trainer(model, optimizer, None, criterion, device, ckpt_dir)
    
    print("\\nExecuting 1-Epoch Forward/Backward Loop (Batch Size = 2)...")
    loss, batch_losses = trainer.train_epoch(dataloader)
    
    half_pt = len(batch_losses) // 2
    first_half_avg = np.mean(batch_losses[:half_pt])
    second_half_avg = np.mean(batch_losses[half_pt:])
    
    print(f"\\nEpoch Complete. Average Loss: {loss:.4f}")
    print(f"First 10 Batch Losses: {[round(l, 4) for l in batch_losses[:10]]}")
    print(f"Last 10 Batch Losses:  {[round(l, 4) for l in batch_losses[-10:]]}")
    print(f"---")
    print(f"First Half Average Loss:  {first_half_avg:.4f}")
    print(f"Second Half Average Loss: {second_half_avg:.4f}")
    
    print("\\nTesting Checkpoint I/O...")
    trainer.save_checkpoint(epoch=1, val_loss=loss, is_best=True)
    
    best_model_path = os.path.join(ckpt_dir, "best_model.pt")
    checkpoint = torch.load(best_model_path, map_location=device)
    print("Checkpoint loaded. Keys:", list(checkpoint.keys()))
    
    # Prove weights are real
    model.load_state_dict(checkpoint['model_state_dict'])
    sample_weights = list(model.state_dict().values())[0].flatten()[:3]
    print(f"Sample First Layer Weights from Disk: {sample_weights.tolist()}")
    
    print("\\n[SUCCESS] Kaggle Smoke Test script is complete and ready for deployment.")

if __name__ == "__main__":
    run_smoke_test()
