import sys
import numpy as np
sys.path.insert(0, "C:/Users/Sheran/Desktop/Parkinson")

from src.deep_learning.explainability.statistical_validator import StatisticalValidator

print("="*60)
print("STEP 4 STRESS TEST: CORRELATED VS UNCORRELATED DATA")
print("="*60)

# ---------------------------------------------------------
# TEST 1: RANK CORRELATIONS
# ---------------------------------------------------------
print("\\n[1] RANK CORRELATION TEST")
# Correlated (engineered similarity)
attr_shap_corr = np.array([0.9, 0.8, 0.1, 0.05, -0.2, 0.4, 0.7, -0.1, 0.3, 0.6])
attr_captum_corr = np.array([0.85, 0.7, 0.15, 0.0, -0.3, 0.35, 0.8, -0.2, 0.4, 0.5])
corr_results = StatisticalValidator.compute_rank_correlations(attr_shap_corr, attr_captum_corr)

# Uncorrelated (pure random noise)
np.random.seed(42)
attr_shap_uncorr = np.random.randn(10)
attr_captum_uncorr = np.random.randn(10)
uncorr_results = StatisticalValidator.compute_rank_correlations(attr_shap_uncorr, attr_captum_uncorr)

print(f"{'Metric':<25} | {'Correlated (Fake SHAP/Captum)':<30} | {'Uncorrelated (Pure Noise)':<30}")
print("-" * 90)
for metric in corr_results.keys():
    print(f"{metric:<25} | {corr_results[metric]:<30.4f} | {uncorr_results[metric]:<30.4f}")

# ---------------------------------------------------------
# TEST 2: FOLD-TO-FOLD STABILITY (AGREEMENT SCORE)
# ---------------------------------------------------------
print("\\n[2] ATTRIBUTION AGREEMENT SCORE TEST")
# Correlated Folds (very slight variance)
fold1 = np.array([0.90, 0.80, 0.10, 0.05, -0.20])
fold2 = np.array([0.88, 0.82, 0.12, 0.04, -0.18])
fold3 = np.array([0.91, 0.79, 0.09, 0.06, -0.21])
fold4 = np.array([0.89, 0.81, 0.11, 0.03, -0.19])
fold5 = np.array([0.92, 0.78, 0.08, 0.07, -0.22])
corr_folds = [fold1, fold2, fold3, fold4, fold5]
stability_corr = StatisticalValidator.compute_fold_stability(corr_folds)

# Uncorrelated Folds (pure random noise spanning -1 to 1)
uncorr_folds = [np.random.uniform(-1, 1, 5) for _ in range(5)]
stability_uncorr = StatisticalValidator.compute_fold_stability(uncorr_folds)

print(f"{'Metric':<35} | {'Correlated Folds':<20} | {'Uncorrelated Noise Folds':<20}")
print("-" * 80)
for metric in stability_corr.keys():
    print(f"{metric:<35} | {stability_corr[metric]:<20.4f} | {stability_uncorr[metric]:<20.4f}")

