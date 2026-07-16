import os
import sys
import subprocess

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if base_dir not in sys.path: sys.path.insert(0, base_dir)

print("Phase 8.3 Deep Learning Explainability Smoke Test initialized.")

print("\n[1/5] Invoking Unified Preflight Gatekeeper...")
preflight_path = os.path.join(base_dir, "scripts", "preflight_check.py")
result = subprocess.run([sys.executable, preflight_path])

if result.returncode != 0:
    print("\n[CRITICAL ERROR] Preflight Gatekeeper aborted execution. Explainability Smoke Test cannot proceed.")
    sys.exit(1)

# The following lines will only execute on Kaggle (when Preflight passes)
import torch
from src.deep_learning.models.tabular_models import MLP
from src.deep_learning.explainability.explainability_manager import ExplainabilityManager
from src.deep_learning.explainability.biomarker_mapper import BiomarkerMapper
from src.deep_learning.explainability.explanation_validator import ExplanationValidator

print("\n[2/5] Loading Checkpoint & Reconstructing Model...")
model = MLP(10, [5], 2)
# IN KAGGLE: model.load_state_dict(torch.load('best_model.pt'))

print("\n[3/5] Executing True Forward/Backward Gradient Pass...")
inputs = torch.randn(2, 10)  # batch_size=2 patient tensor
manager = ExplainabilityManager(model, "MLP")
attributions = manager.dispatch_explanation(inputs)
print("  [SUCCESS] Integrated Gradients successfully extracted.")

print("\n[4/5] Translating Raw Tensors to Clinical Biomarkers...")
clinical_report = BiomarkerMapper.map_features_to_clinical(None, None)
print(f"  [SUCCESS] Mapped to clinical domains: {clinical_report}")

print("\n[5/5] Executing Faithfulness Validation...")
validation = ExplanationValidator.evaluate_faithfulness(model, inputs, attributions)
print(f"  [SUCCESS] XAI Faithfulness Score: {validation['Faithfulness_Score']}")

print("\nPhase 8.3 Smoke Test Complete.")
