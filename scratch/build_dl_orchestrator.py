import os

base_dir = "C:/Users/Sheran/Desktop/Parkinson"

script_code = """import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path: sys.path.insert(0, base_dir)

print("Phase 8.1 Deep Learning Orchestrator initialized.")

# STRICT DEPENDENCY ENFORCEMENT: 
# Do not catch this ImportError. The framework must fail natively if not configured for DL.
import torch
from src.deep_learning.utils import DeviceManager, Reproducibility

print("1. Enforcing Global Reproducibility...")
Reproducibility.seed_everything(42)

print("2. Initializing Device Manager...")
device = DeviceManager.get_device()
print(f"  [INFO] Training automatically mapped to: {device}")

print("3. Instantiating Tabular Deep Learning Architectures...")
from src.deep_learning.models.tabular_models import MLP, ResNetTabular, TabNetWrapper

# In Kaggle this will proceed to train_epoch over the DataLoader.
print("Phase 8.1 Structural Execution Complete.")
"""
with open(os.path.join(base_dir, "scripts/run_dl_benchmarks.py"), "w") as f: f.write(script_code)

print("Scaffolded Phase 8.1 Orchestrator Script.")
