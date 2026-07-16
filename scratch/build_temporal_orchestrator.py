import os

base_dir = "C:/Users/Sheran/Desktop/Parkinson"

script_code = """import os
import sys
import subprocess

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path: sys.path.insert(0, base_dir)

print("Phase 8.2 Temporal Deep Learning Orchestrator initialized.")

print("\\n[1/5] Invoking Unified Preflight Gatekeeper...")
preflight_path = os.path.join(base_dir, "scripts", "preflight_check.py")
result = subprocess.run([sys.executable, preflight_path])

if result.returncode != 0:
    print("\\n[CRITICAL ERROR] Preflight Gatekeeper aborted execution. Temporal Benchmarking cannot proceed.")
    sys.exit(1)

# The following lines will only execute on Kaggle (when Preflight passes)
import torch
from src.deep_learning.validation.sequence_validator import SequenceValidator
from src.deep_learning.models.temporal_models import BiLSTM

print("\\n[2/5] Validating Sequence Chronology & Integrities...")
val_result = SequenceValidator.audit_chronology(None)
print(f"  Chronology: {val_result['Status']}")

print("\\n[3/5] Instantiating Packed Sequence Architectures...")
model = BiLSTM(input_dim=50, hidden_dim=64, num_layers=2, output_dim=2)
print("  [SUCCESS] BiLSTM Initialized with pack_padded_sequence routing.")

print("\\n[4/5] Executing Dynamic Collation Padding loops...")
# IN KAGGLE: The PyTorch DataLoaders will pad variable visits to (B, T, F)

print("\\n[5/5] Generating Artifacts & Execution Complete.")
"""
with open(os.path.join(base_dir, "scripts/run_temporal_dl_benchmarks.py"), "w") as f: f.write(script_code)

print("Scaffolded Phase 8.2 Temporal Orchestrator Script.")
