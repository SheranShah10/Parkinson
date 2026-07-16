import sys
import numpy as np
sys.path.insert(0, "C:/Users/Sheran/Desktop/Parkinson")

from src.deep_learning.explainability.statistical_validator import StatisticalValidator

print("="*60)
print("STEP 4: XAI STATISTICAL VALIDATOR (SCIPY/NUMPY)")
print("="*60)

print("\\n[HONEST AUDIT] Upstream XAI Harness Validation:")
print("The upstream harness (`captum_wrapper.py` and `shap_wrapper.py`) cannot save real PyTorch gradients locally because PyTorch installation failed. They are currently stubbed. Therefore, this test validates the true scipy/numpy mathematical logic using SYNTHESIZED numpy gradients.")

# 1. Test Rank Correlations
print("\\n--- Testing Real Spearman & Kendall Tau Math ---")
# Simulate Feature Attributions for 10 features from two different XAI methods
attr_shap = np.array([0.9, 0.8, 0.1, 0.05, -0.2, 0.4, 0.7, -0.1, 0.3, 0.6])
attr_captum = np.array([0.85, 0.7, 0.15, 0.0, -0.3, 0.35, 0.8, -0.2, 0.4, 0.5])

correlations = StatisticalValidator.compute_rank_correlations(attr_shap, attr_captum)
for k, v in correlations.items():
    print(f"{k}: {v:.4f}")

# 2. Test Fold Stability
print("\\n--- Testing Real Fold-to-Fold Stability & Agreement Score ---")
# Simulate 5 folds of attributions for the same 10 features
fold1 = np.array([0.90, 0.80, 0.10, 0.05, -0.20])
fold2 = np.array([0.88, 0.82, 0.12, 0.04, -0.18])
fold3 = np.array([0.91, 0.79, 0.09, 0.06, -0.21])
fold4 = np.array([0.89, 0.81, 0.11, 0.03, -0.19])
fold5 = np.array([0.92, 0.78, 0.08, 0.07, -0.22])

fold_list = [fold1, fold2, fold3, fold4, fold5]

stability = StatisticalValidator.compute_fold_stability(fold_list)
for k, v in stability.items():
    print(f"{k}: {v:.4f}")

