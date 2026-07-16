import os

base_dir = "C:/Users/Sheran/Desktop/Parkinson"

script_code = """import os
import sys

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path: sys.path.insert(0, base_dir)

from src.utils.preflight.hardware_validator import HardwareValidator
from src.utils.preflight.version_validator import VersionValidator
from src.utils.preflight.dry_run_validator import DryRunValidator

print("========================================")
print("DEEP LEARNING PREFLIGHT VALIDATION")
print("========================================")

score = 100
reports = []

print("1. Validating Versions & Feature Store...")
v_audit = VersionValidator.audit()
if v_audit["Status"] != "PASS": score -= 20
reports.append(f"- Version Integrity: {v_audit['Status']}")

print("2. Validating Hardware & Environment...")
h_audit = HardwareValidator.audit()
if h_audit["Status"] != "PASS": score -= 40
reports.append(f"- Hardware Readiness: {h_audit['Status']} (GPUs: {h_audit.get('GPUs', 0)})")

print("3. Executing Deep Learning Dry-Run (batch_size=2)...")
d_audit = DryRunValidator.execute_dry_run()
if d_audit["Status"] != "PASS": score -= 40
reports.append(f"- Dry-Run Engine: {d_audit['Status']} ({d_audit['Message']})")

print("\\n========================================")
print(f"BENCHMARK READINESS SCORE: {score}/100")
print("========================================")
for r in reports: print(r)

if score < 100:
    print("\\n[CRITICAL ERROR] Preflight Validation Failed.")
    print("Execution aborted. Please resolve dependencies before triggering Kaggle training.")
    sys.exit(1)
else:
    print("\\n[SUCCESS] Preflight Complete. You are cleared for Kaggle Execution!")
"""
with open(os.path.join(base_dir, "scripts/preflight_check.py"), "w") as f: f.write(script_code)

print("Scaffolded scripts/preflight_check.py.")
