import os
import sys
import pandas as pd

sys.path.insert(0, "C:/Users/Sheran/Desktop/Parkinson")

from src.utils.preflight.dry_run_validator import DryRunValidator
from src.utils.preflight.version_validator import VersionValidator
from src.benchmark.performance.hardware_monitor import HardwareMonitor

print("="*60)
print("STEP 2A: EXECUTING REWRITTEN PREFLIGHT STUBS")
print("="*60)

# 1. Hardware Monitor Output
print("\\n--- Testing Hardware Monitor (psutil/torch) ---")
hw_stats = HardwareMonitor.get_hardware_stats()
for k, v in hw_stats.items():
    print(f"{k}: {v}")

# 2. Version Validator Output
print("\\n--- Testing Version Validator (Real File Hashing) ---")
v_stats = VersionValidator.audit()
for k, v in v_stats.items():
    print(f"{k}: {v}")

# 3. Dry-Run Validator Output
print("\\n--- Testing Dry-Run Validator (Real PyTorch Forward Pass) ---")
dr_stats = DryRunValidator.execute_dry_run()
for k, v in dr_stats.items():
    print(f"{k}: {v}")
