import os
import math
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold
from sklearn.metrics import f1_score, roc_auc_score, balanced_accuracy_score

# =========================================================
# 1. ARCHITECTURE DEFINITIONS
# =========================================================
# (Include TabNetWrapper, SAINT, WideDeep from tabular_models.py)
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
        output = output.view(original_size)
        return output

class TabNetWrapper(nn.Module):
    def __init__(self, input_dim, n_d=8, n_a=8, n_steps=3, gamma=1.3, output_dim=2):
        super().__init__()
        self.n_d = n_d
        self.n_a = n_a
        self.n_steps = n_steps
        self.gamma = gamma
        self.initial_bn = nn.BatchNorm1d(input_dim)
        
        self.feature_transformers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(input_dim, (n_d + n_a) * 2),
                nn.BatchNorm1d((n_d + n_a) * 2),
                nn.GLU(dim=-1)
            ) for _ in range(n_steps)
        ])
        self.attentive_transformers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(n_a, input_dim),
                nn.BatchNorm1d(input_dim),
                Sparsemax(dim=-1)
            ) for _ in range(n_steps)
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
            masked_x = x * mask
            ft_out = self.feature_transformers[step](masked_x)
            d = ft_out[:, :self.n_d]
            a_prev = ft_out[:, self.n_d:]
            out_accumulator = out_accumulator + d
        return self.final_mapping(out_accumulator)

class SAINTBlock(nn.Module):
    def __init__(self, d_model, num_heads, dropout):
        super().__init__()
        self.feature_attention = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.intersample_attention = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.ffn = nn.Sequential(nn.Linear(d_model, d_model * 4), nn.ReLU(), nn.Dropout(dropout), nn.Linear(d_model * 4, d_model))
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
        x_norm = self.ln3(x)
        x = x + self.ffn(x_norm)
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

# =========================================================
# 2. VERIFICATION PROTOCOL
# =========================================================
def get_data():
    input_dir = "/kaggle/input"
    fs_path = None
    for root, dirs, files in os.walk(input_dir):
        if "master_features.parquet" in files:
            fs_path = os.path.join(root, "master_features.parquet")
            break
            
    df = pd.read_parquet(fs_path)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    raw_values = df[numeric_cols].values
    
    imputer = SimpleImputer(strategy='median')
    processed_values = StandardScaler().fit_transform(imputer.fit_transform(raw_values))
    
    median_val = np.median(processed_values[:, 0])
    y_full = (processed_values[:, 0] > median_val).astype(int)
    processed_values = processed_values[:, 1:] # Zero-leakage
    
    groups = df['PATNO'].values
    train_idx, val_idx = next(GroupKFold(n_splits=5).split(processed_values, y_full, groups))
    
    X_train = torch.tensor(processed_values[train_idx], dtype=torch.float32)
    y_train = torch.tensor(y_full[train_idx], dtype=torch.long)
    X_val = torch.tensor(processed_values[val_idx], dtype=torch.float32)
    y_val = torch.tensor(y_full[val_idx], dtype=torch.long)
    
    return X_train, y_train, X_val, y_val

def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)

def verify_architecture(name, model, dataloader_train, dataloader_val, device):
    print(f"\\n--- VERIFYING {name} ---")
    model = model.to(device)
    optimizer = optim.AdamW(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()
    scaler = torch.amp.GradScaler('cuda') if torch.cuda.is_available() else None
    
    results = {"Name": name, "Status": "PASS"}
    results["Params"] = sum(p.numel() for p in model.parameters())
    
    torch.cuda.reset_peak_memory_stats()
    start_time = time.time()
    
    model.train()
    grad_ok = False
    mixed_precision_ok = True
    
    # Check 1: Training & Gradients
    for X, y in dataloader_train:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        try:
            if scaler:
                with torch.amp.autocast('cuda'):
                    out = model(X)
                    loss = criterion(out, y)
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
            else:
                out = model(X)
                loss = criterion(out, y)
                loss.backward()
                optimizer.step()
        except Exception as e:
            results["Status"] = f"FAIL (Mixed-Precision/Forward): {e}"
            mixed_precision_ok = False
            break
            
        # Check Gradients
        for param in model.parameters():
            if param.grad is not None and torch.sum(torch.abs(param.grad)) > 0:
                grad_ok = True
                break
        break # Just 1 batch for gradient check
        
    results["Gradient Flow"] = "PASS" if grad_ok else "FAIL"
    
    # Full Epoch Training
    for X, y in dataloader_train:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        with torch.amp.autocast('cuda'):
            out = model(X)
            loss = criterion(out, y)
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()
        
    results["Train Time (s)"] = round(time.time() - start_time, 2)
    results["Peak GPU Mem (MB)"] = round(torch.cuda.max_memory_allocated() / 1024 / 1024, 2)
    
    # Check 2: Validation & Inference
    model.eval()
    all_preds, all_probs, all_targets = [], [], []
    with torch.no_grad():
        for X, y in dataloader_val:
            X, y = X.to(device), y.to(device)
            out = model(X)
            probs = torch.softmax(out, dim=1)[:, 1]
            preds = torch.argmax(out, dim=1)
            all_probs.extend(probs.cpu().numpy())
            all_preds.extend(preds.cpu().numpy())
            all_targets.extend(y.cpu().numpy())
            
    try:
        results["F1"] = round(f1_score(all_targets, all_preds), 4)
        results["ROC-AUC"] = round(roc_auc_score(all_targets, all_probs), 4)
        results["Balanced Acc"] = round(balanced_accuracy_score(all_targets, all_preds), 4)
    except:
        results["F1"] = results["ROC-AUC"] = results["Balanced Acc"] = "NaN"
        
    # Check 3: Checkpointing
    ckpt_path = f"/kaggle/working/{name}_ckpt.pt"
    torch.save(model.state_dict(), ckpt_path)
    if os.path.exists(ckpt_path):
        results["Checkpoint"] = "PASS"
    else:
        results["Checkpoint"] = "FAIL"
        
    if results["Gradient Flow"] == "FAIL" or results["Status"] != "PASS" or results["F1"] == "NaN":
        results["Status"] = "FAIL"
        
    return results

def run_verification_protocol():
    set_seed(42)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    X_train, y_train, X_val, y_val = get_data()
    input_dim = X_train.shape[1]
    
    train_loader = DataLoader(TensorDataset(X_train, y_train), batch_size=32, shuffle=True)
    val_loader = DataLoader(TensorDataset(X_val, y_val), batch_size=32, shuffle=False)
    
    models = {
        "TabNet": TabNetWrapper(input_dim=input_dim),
        "SAINT": SAINT(input_dim=input_dim, d_model=32, num_heads=4, num_blocks=1, output_dim=2),
        "WideDeep": WideDeep(input_dim=input_dim, deep_hidden_dims=[64, 32], output_dim=2)
    }
    
    report = []
    for name, model in models.items():
        res = verify_architecture(name, model, train_loader, val_loader, device)
        report.append(res)
        
    print("\n============================================================")
    print("PHASE 8.5: ARCHITECTURE VERIFICATION REPORT")
    print("============================================================")
    df_report = pd.DataFrame(report)
    print(df_report.to_markdown(index=False))

if __name__ == "__main__":
    run_verification_protocol()
