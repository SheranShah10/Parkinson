import os

base_dir = "C:/Users/Sheran/Desktop/Parkinson"
dirs = [
    "configs/deep_learning",
    "src/deep_learning/data",
    "src/deep_learning/training",
    "src/deep_learning/models",
    "artifacts/deep_learning/models",
    "artifacts/deep_learning/predictions",
    "artifacts/deep_learning/embeddings",
    "artifacts/deep_learning/attention",
    "artifacts/deep_learning/feature_importance",
    "artifacts/deep_learning/training_curves",
    "artifacts/deep_learning/logs"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    if d.startswith("src/"):
        with open(os.path.join(base_dir, d, "__init__.py"), "w") as f: f.write("")

# 1. Reproducibility & Device Manager
device_code = """import os
import random
import numpy as np

class DeviceManager:
    @staticmethod
    def get_device():
        import torch
        if torch.cuda.is_available(): return torch.device("cuda")
        if torch.backends.mps.is_available(): return torch.device("mps")
        return torch.device("cpu")

class Reproducibility:
    @staticmethod
    def seed_everything(seed=42):
        import torch
        random.seed(seed)
        os.environ['PYTHONHASHSEED'] = str(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
"""
with open(os.path.join(base_dir, "src/deep_learning/utils.py"), "w") as f: f.write(device_code)

# 2. Advanced Training Loop
trainer_code = """import os
import json

class Trainer:
    def __init__(self, model, optimizer, scheduler, criterion, device):
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = criterion
        self.device = device
        import torch
        self.scaler = torch.cuda.amp.GradScaler() if torch.cuda.is_available() else None

    def train_epoch(self, dataloader):
        import torch
        self.model.train()
        total_loss = 0
        for X, y in dataloader:
            X, y = X.to(self.device), y.to(self.device)
            self.optimizer.zero_grad()
            
            if self.scaler:
                with torch.cuda.amp.autocast():
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
"""
with open(os.path.join(base_dir, "src/deep_learning/training/trainer.py"), "w") as f: f.write(trainer_code)

# 3. Model Wrappers
models_code = """class MLP: pass
class ResNetTabular: pass
class FT_Transformer: pass
class TabNetWrapper: pass
class TabTransformer: pass
class SAINT: pass
class WideDeep: pass
"""
with open(os.path.join(base_dir, "src/deep_learning/models/tabular_models.py"), "w") as f: f.write(models_code)

print("Scaffolded Phase 8.1 DL Directories, Reproducibility Engine, and Trainer.")
