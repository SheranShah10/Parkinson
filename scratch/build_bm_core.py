import os

base_dir = "C:/Users/Sheran/Desktop/Parkinson"
dirs = [
    "configs/benchmark",
    "src/benchmark/performance",
    "src/models/base",
    "src/metrics",
    "src/explainability",
    "artifacts/models",
    "artifacts/predictions",
    "artifacts/metrics",
    "artifacts/feature_importance",
    "artifacts/confusion_matrices",
    "artifacts/roc_curves",
    "artifacts/calibration",
    "artifacts/logs",
    "artifacts/timings",
    "leaderboard",
    "logs",
    "reports/statistics",
    "reports/publication/tables",
    "reports/publication/figures",
    "reports/publication/latex",
    "reports/performance",
    "metadata/dashboard",
    "docs/paper",
    "docs/architecture"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    if d.startswith("src/"):
        with open(os.path.join(base_dir, d, "__init__.py"), "w") as f: f.write("")

# 1. Base Model Interface
model_code = """class BaseModelInterface:
    def initialize(self, config): raise NotImplementedError
    def fit(self, X, y): raise NotImplementedError
    def predict(self, X): raise NotImplementedError
    def predict_proba(self, X): raise NotImplementedError
    def save(self, path): raise NotImplementedError
    def load(self, path): raise NotImplementedError
    def export_metadata(self): return {}
"""
with open(os.path.join(base_dir, "src/models/base/base_model.py"), "w") as f: f.write(model_code)

# 2. Native Numpy Metrics Engine
metric_code = """import numpy as np

def accuracy_score(y_true, y_pred):
    return np.mean(y_true == y_pred)

def f1_score_macro(y_true, y_pred):
    classes = np.unique(y_true)
    f1s = []
    for c in classes:
        tp = np.sum((y_pred == c) & (y_true == c))
        fp = np.sum((y_pred == c) & (y_true != c))
        fn = np.sum((y_pred != c) & (y_true == c))
        if (tp+fp) == 0 and (tp+fn) == 0: continue
        prec = tp / (tp + fp) if (tp+fp)>0 else 0
        rec = tp / (tp + fn) if (tp+fn)>0 else 0
        f1 = 2 * (prec * rec) / (prec + rec) if (prec+rec)>0 else 0
        f1s.append(f1)
    return np.mean(f1s) if f1s else 0.0

def rmse_score(y_true, y_pred):
    return np.sqrt(np.mean((y_true - y_pred)**2))

def mae_score(y_true, y_pred):
    return np.mean(np.abs(y_true - y_pred))
"""
with open(os.path.join(base_dir, "src/metrics/native_metrics.py"), "w") as f: f.write(metric_code)

# 3. Performance Monitor Mock
perf_code = """import time
import json
import psutil

class HardwareMonitor:
    def get_profile(self):
        return {
            'CPU_Percent': psutil.cpu_percent(),
            'RAM_Percent': psutil.virtual_memory().percent,
            'GPU_Available': False
        }
"""
with open(os.path.join(base_dir, "src/benchmark/performance/hardware_monitor.py"), "w") as f: f.write(perf_code)

print("Scaffolded Phase 6.4 Core Directories and Modules.")
