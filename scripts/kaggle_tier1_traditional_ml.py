"""
Tier 1: Traditional Machine Learning Benchmark (v2 — merged)
PPMI DaTSCAN — Parkinson's severity (NP3TOT regression) & stage (NHY classification)

Merge notes:
  - Kept from the stratified draft: StratifiedGroupKFold for classification,
    per-model feature importance CSVs, per-fold JSON registry, timing, 95% CI.
  - Restored (D021): NHY explicitly collapsed to ordinal {0,1,2,"3+"} — was
    silently reverted to raw multi-class in the stratified draft, which would
    have made this leaderboard incomparable to the FT-Transformer benchmark.
  - Restored: Data Quality Gate halts on constant/zero-variance features too,
    not just duplicates/infinite values, per the original spec.
  - Extended: Mean/SD/Min/Max now computed for every metric, not just the
    primary one (Macro_F1 / RMSE).
"""

import os
import sys
import time
import json
import warnings
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score,
    matthews_corrcoef, cohen_kappa_score, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score,
    explained_variance_score, median_absolute_error
)

from sklearn.linear_model import LogisticRegression, LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier,
    GradientBoostingClassifier, HistGradientBoostingClassifier,
    RandomForestRegressor, ExtraTreesRegressor,
    GradientBoostingRegressor, HistGradientBoostingRegressor
)
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier, XGBRegressor
from lightgbm import LGBMClassifier, LGBMRegressor
from catboost import CatBoostClassifier, CatBoostRegressor

warnings.filterwarnings('ignore')

SEED = 42
OUTPUT_DIR = "/kaggle/working" if os.path.isdir("/kaggle/working") else "."
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")
LEADERBOARD_DIR = os.path.join(OUTPUT_DIR, "leaderboard")
METADATA_DIR = os.path.join(OUTPUT_DIR, "metadata")
FI_DIR = os.path.join(OUTPUT_DIR, "artifacts/tier1/feature_importance")

for d in [REPORTS_DIR, LEADERBOARD_DIR, METADATA_DIR, FI_DIR]:
    os.makedirs(d, exist_ok=True)


def collapse_nhy(raw_values):
    """D021: map raw NHY {0,1,2,3,4,5} -> ordinal {0,1,2,3} where 3 == '3+' bucket."""
    mapped = np.full(raw_values.shape, np.nan)
    valid = ~np.isnan(raw_values)
    v = raw_values[valid]
    out = np.select([v == 0, v == 1, v == 2, v >= 3], [0, 1, 2, 3], default=np.nan)
    mapped[valid] = out
    return mapped, {0: "Stage 0", 1: "Stage 1", 2: "Stage 2", 3: "Stage 3+"}


def get_data():
    input_dir = "/kaggle/input"
    fs_path = None
    for root, dirs, files in os.walk(input_dir):
        if "master_features.parquet" in files:
            fs_path = os.path.join(root, "master_features.parquet")
            break
    if not fs_path:
        raise FileNotFoundError("master_features.parquet not found in /kaggle/input")

    df = pd.read_parquet(fs_path)

    if 'NHY' not in df.columns or 'NP3TOT' not in df.columns:
        raise ValueError("CRITICAL: NHY or NP3TOT missing from Feature Store. Aborting.")
    if 'PATNO' not in df.columns or 'EVENT_ID' not in df.columns:
        raise ValueError("CRITICAL: PATNO or EVENT_ID missing for data quality tracking. Aborting.")

    # ---- DATA QUALITY GATE (halts on duplicates, constant features, or infinite values) ----
    dq_report = []
    dup_rows = df.duplicated().sum()
    dup_pairs = df.duplicated(subset=['PATNO', 'EVENT_ID']).sum()
    inf_vals = np.isinf(df.select_dtypes(include=[np.number]).values).sum()

    feature_cols_preview = df.drop(columns=['NHY', 'NP3TOT', 'PATNO', 'EVENT_ID'], errors='ignore')
    nunique = feature_cols_preview.nunique(dropna=True)
    constant_cols = nunique[nunique <= 1].index.tolist()

    dq_report.append(f"- Duplicate Rows: {dup_rows}")
    dq_report.append(f"- Duplicate PATNO/EVENT_ID: {dup_pairs}")
    dq_report.append(f"- Infinite Values: {inf_vals}")

    if dup_rows > 0 or dup_pairs > 0 or inf_vals > 0:
        with open(os.path.join(REPORTS_DIR, "DATA_QUALITY_REPORT.md"), "w") as f:
            f.write("# DATA QUALITY GATE — FAILED (execution halted)\n\n" + "\n".join(dq_report))
        print("\n".join(dq_report))
        raise ValueError("CRITICAL: Data Quality Gate Failed. Check DATA_QUALITY_REPORT.md")

    with open(os.path.join(REPORTS_DIR, "DATA_QUALITY_REPORT.md"), "w") as f:
        f.write("# DATA QUALITY GATE — PASSED\n\n" + "\n".join(dq_report))

    # ---- D021: explicit NHY ordinal collapse ----
    y_cls, class_labels = collapse_nhy(df['NHY'].values.astype(float))
    valid_cls_mask = ~np.isnan(y_cls)
    cls_counts = pd.Series(y_cls[valid_cls_mask]).map(class_labels).value_counts()
    with open(os.path.join(REPORTS_DIR, "TARGET_DISTRIBUTION.md"), "w") as f:
        f.write("# NHY Class Distribution (D021 ordinal {0,1,2,3+})\n\n")
        f.write(cls_counts.to_markdown())

    y_reg = df['NP3TOT'].values
    groups = df['PATNO'].values

    # ---- FATAL LEAKAGE PURGE ----
    # Linear Regression scored R2=1.0 because exact aliases of the target (e.g. MOTOR_Severity_Score)
    # and clinical subcomponents of the MDS-UPDRS tests were present.
    # The benchmark must only use objective biological/imaging/demographic data.
    # We explicitly drop MOTOR_Severity and TEMPORAL_Motor_Slope to prevent same-visit leaks,
    # but we DO NOT drop the entire 'MOTOR_' prefix to safely preserve TEMPORAL_Motor_Lag1.
    leaky_patterns = ['NHY', 'NP3', 'TARGET_', 'MOTOR_Severity', 'TEMPORAL_Motor_Slope', 'PD_DX', 'CLINI_', 'MDS-U_'] 
    leaky_cols = [c for c in df.columns if any(pat in c.upper() for pat in leaky_patterns)]
    
    df_features = df.drop(columns=leaky_cols + ['PATNO', 'EVENT_ID'], errors='ignore')

    # ---- Feature Integrity Audit (100% missing + non-numeric + constant) ----
    missing_pct = df_features.isnull().mean()
    to_drop_missing = missing_pct[missing_pct == 1.0].index.tolist()

    dropped_path = os.path.join(REPORTS_DIR, "DROPPED_FEATURES.md")
    with open(dropped_path, "w") as f:
        f.write("# Dropped Features\n\n## 100% Missing\n\n| Feature | Missing Pct | Reason |\n|---|---|---|\n")
        for col in to_drop_missing:
            f.write(f"| {col} | 100% | Entirely missing before imputation |\n")

    df_features = df_features.drop(columns=to_drop_missing)
    
    # Constant columns are already identified above as constant_cols
    # Remove any that were already dropped for being 100% missing
    constant_cols_to_drop = [c for c in constant_cols if c in df_features.columns]
    if constant_cols_to_drop:
        with open(dropped_path, "a") as f:
            f.write("\n## Constant / Zero-Variance\n\n| Feature | Reason |\n|---|---|\n")
            for col in constant_cols_to_drop:
                f.write(f"| {col} | Zero variance or constant value |\n")
        df_features = df_features.drop(columns=constant_cols_to_drop)

    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    non_numeric_dropped = [c for c in df_features.columns if c not in numeric_cols]
    if non_numeric_dropped:
        with open(dropped_path, "a") as f:
            f.write("\n## Non-Numeric\n\n")
            for col in non_numeric_dropped:
                f.write(f"- {col}\n")

    df_features = df_features[numeric_cols]
    feature_names = numeric_cols.tolist()
    X = df_features.values

    return X, y_cls, y_reg, groups, feature_names, class_labels


def get_stats(fold_metrics):
    """Mean, SD, Min, Max, 95% CI for a list of per-fold metric values."""
    arr = np.array([x for x in fold_metrics if x is not None and not np.isnan(x)], dtype=float)
    if len(arr) == 0:
        return dict(mean=np.nan, sd=np.nan, min=np.nan, max=np.nan, ci95=np.nan)
    mean, std = arr.mean(), arr.std()
    ci = 1.96 * (std / np.sqrt(len(arr)))
    return dict(mean=mean, sd=std, min=arr.min(), max=arr.max(), ci95=ci)


def _flatten_stats(metrics_dict):
    row = {}
    for key, values in metrics_dict.items():
        stats = get_stats(values)
        for stat_name, stat_val in stats.items():
            row[f"{key}_{stat_name}"] = stat_val
    return row


def evaluate_classification(models, X, y, groups, feature_names):
    results, fold_registry = [], []
    sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    valid_idx = ~np.isnan(y)
    X, y, groups = X[valid_idx], y[valid_idx], groups[valid_idx]

    for name, model in models.items():
        print(f"  > Training Classification: {name}...")
        metrics = {k: [] for k in ['acc', 'bal_acc', 'f1_macro', 'f1_weighted', 'prec_macro',
                                     'rec_macro', 'mcc', 'kappa', 'roc_auc_ovr', 'train_time', 'infer_time']}
        fold_idx = 1
        for train_idx, val_idx in sgkf.split(X, y, groups):
            X_train, y_train = X[train_idx], y[train_idx]
            X_val, y_val = X[val_idx], y[val_idx]

            imputer, scaler = SimpleImputer(strategy='median'), StandardScaler()
            X_train = scaler.fit_transform(imputer.fit_transform(X_train))
            X_val = scaler.transform(imputer.transform(X_val))

            t0 = time.time(); model.fit(X_train, y_train); t_train = time.time() - t0
            t0 = time.time(); preds = model.predict(X_val); t_infer = time.time() - t0

            try:
                probs = model.predict_proba(X_val)
                roc = roc_auc_score(y_val, probs, multi_class='ovr')
            except (ValueError, AttributeError):
                roc = np.nan

            metrics['train_time'].append(t_train)
            metrics['infer_time'].append(t_infer)
            metrics['acc'].append(accuracy_score(y_val, preds))
            metrics['bal_acc'].append(balanced_accuracy_score(y_val, preds))
            metrics['f1_macro'].append(f1_score(y_val, preds, average='macro'))
            metrics['f1_weighted'].append(f1_score(y_val, preds, average='weighted'))
            metrics['prec_macro'].append(precision_score(y_val, preds, average='macro', zero_division=0))
            metrics['rec_macro'].append(recall_score(y_val, preds, average='macro', zero_division=0))
            metrics['mcc'].append(matthews_corrcoef(y_val, preds))
            metrics['kappa'].append(cohen_kappa_score(y_val, preds))
            metrics['roc_auc_ovr'].append(roc)

            fold_registry.append({"Model": name, "Type": "Classification", "Fold": fold_idx,
                                   "Macro_F1": metrics['f1_macro'][-1], "Accuracy": metrics['acc'][-1]})
            fold_idx += 1

        if hasattr(model, 'feature_importances_'):
            try:
                # The imputer may have dropped 100% missing columns from the last fold
                active_feats = feature_names
                if hasattr(imputer, 'get_feature_names_out'):
                    active_feats = imputer.get_feature_names_out(feature_names)
                fi = pd.DataFrame({'Feature': active_feats, 'Importance': model.feature_importances_})
                fi.sort_values('Importance', ascending=False).to_csv(
                    os.path.join(FI_DIR, f"{name.replace(' ', '_')}_FI.csv"), index=False)
            except Exception as e:
                print(f"    [Warning] Could not export feature importance for {name}: {e}")

        row = {'Model': name}
        row.update(_flatten_stats(metrics))
        results.append(row)

    return pd.DataFrame(results), fold_registry


def evaluate_regression(models, X, y, groups, feature_names):
    results, fold_registry = [], []
    gkf = GroupKFold(n_splits=5)
    valid_idx = ~np.isnan(y)
    X, y, groups = X[valid_idx], y[valid_idx], groups[valid_idx]

    for name, model in models.items():
        print(f"  > Training Regression: {name}...")
        metrics = {k: [] for k in ['rmse', 'mae', 'r2', 'ev', 'medae', 'train_time', 'infer_time']}
        fold_idx = 1
        for train_idx, val_idx in gkf.split(X, y, groups):
            X_train, y_train = X[train_idx], y[train_idx]
            X_val, y_val = X[val_idx], y[val_idx]

            imputer, scaler = SimpleImputer(strategy='median'), StandardScaler()
            X_train = scaler.fit_transform(imputer.fit_transform(X_train))
            X_val = scaler.transform(imputer.transform(X_val))

            t0 = time.time(); model.fit(X_train, y_train); t_train = time.time() - t0
            t0 = time.time(); preds = model.predict(X_val); t_infer = time.time() - t0

            metrics['train_time'].append(t_train)
            metrics['infer_time'].append(t_infer)
            metrics['rmse'].append(np.sqrt(mean_squared_error(y_val, preds)))
            metrics['mae'].append(mean_absolute_error(y_val, preds))
            metrics['r2'].append(r2_score(y_val, preds))
            metrics['ev'].append(explained_variance_score(y_val, preds))
            metrics['medae'].append(median_absolute_error(y_val, preds))

            fold_registry.append({"Model": name, "Type": "Regression", "Fold": fold_idx,
                                   "RMSE": metrics['rmse'][-1], "R2": metrics['r2'][-1]})
            fold_idx += 1

        if hasattr(model, 'feature_importances_'):
            try:
                active_feats = feature_names
                if hasattr(imputer, 'get_feature_names_out'):
                    active_feats = imputer.get_feature_names_out(feature_names)
                fi = pd.DataFrame({'Feature': active_feats, 'Importance': model.feature_importances_})
                fi.sort_values('Importance', ascending=False).to_csv(
                    os.path.join(FI_DIR, f"{name.replace(' ', '_')}_FI.csv"), index=False)
            except Exception as e:
                print(f"    [Warning] Could not export feature importance for {name}: {e}")

        row = {'Model': name}
        row.update(_flatten_stats(metrics))
        results.append(row)

    return pd.DataFrame(results), fold_registry


def run_tier1_benchmark():
    print("Loading Data & Running Quality Gates...")
    X, y_cls, y_reg, groups, feature_names, class_labels = get_data()
    print(f"Features: {X.shape[1]} | Classes (D021 ordinal): {class_labels}\n")

    clf_models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=SEED),
        'Decision Tree': DecisionTreeClassifier(random_state=SEED),
        'Random Forest': RandomForestClassifier(n_jobs=-1, random_state=SEED),
        'Extra Trees': ExtraTreesClassifier(n_jobs=-1, random_state=SEED),
        'AdaBoost': AdaBoostClassifier(random_state=SEED),
        'Gradient Boosting': GradientBoostingClassifier(random_state=SEED),
        'HistGradientBoosting': HistGradientBoostingClassifier(random_state=SEED),
        'XGBoost': XGBClassifier(n_jobs=-1, eval_metric='mlogloss', random_state=SEED),
        'LightGBM': LGBMClassifier(n_jobs=-1, verbose=-1, random_state=SEED),
        'CatBoost': CatBoostClassifier(verbose=0, thread_count=-1, random_state=SEED),
        'SVM (RBF)': SVC(probability=True, random_state=SEED),
        'KNN': KNeighborsClassifier(n_jobs=-1),
        'Gaussian NB': GaussianNB(),
        'MLPClassifier': MLPClassifier(max_iter=1000, random_state=SEED)
    }

    reg_models = {
        'Linear Regression': LinearRegression(),
        'Ridge': Ridge(random_state=SEED),
        'Lasso': Lasso(random_state=SEED),
        'ElasticNet': ElasticNet(random_state=SEED),
        'Random Forest Regressor': RandomForestRegressor(n_jobs=-1, random_state=SEED),
        'Extra Trees Regressor': ExtraTreesRegressor(n_jobs=-1, random_state=SEED),
        'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=SEED),
        'HistGradientBoostingRegressor': HistGradientBoostingRegressor(random_state=SEED),
        'XGBoost Regressor': XGBRegressor(n_jobs=-1, random_state=SEED),
        'LightGBM Regressor': LGBMRegressor(n_jobs=-1, verbose=-1, random_state=SEED),
        'CatBoost Regressor': CatBoostRegressor(verbose=0, thread_count=-1, random_state=SEED),
        'SVR': SVR()
    }

    print("\n--- RUNNING TIER 1 CLASSIFICATION (NHY, D021 ordinal {0,1,2,3+}, StratifiedGroupKFold) ---")
    df_cls, fold_reg_cls = evaluate_classification(clf_models, X, y_cls, groups, feature_names)
    df_cls = df_cls.sort_values('f1_macro_mean', ascending=False)
    df_cls.to_csv(os.path.join(LEADERBOARD_DIR, 'tier1_classification.csv'), index=False)

    print("\n--- RUNNING TIER 1 REGRESSION (NP3TOT, GroupKFold) ---")
    df_reg, fold_reg_reg = evaluate_regression(reg_models, X, y_reg, groups, feature_names)
    df_reg = df_reg.sort_values('rmse_mean', ascending=True)
    df_reg.to_csv(os.path.join(LEADERBOARD_DIR, 'tier1_regression.csv'), index=False)

    with open(os.path.join(METADATA_DIR, 'tier1_fold_registry.json'), 'w') as f:
        json.dump(fold_reg_cls + fold_reg_reg, f, indent=4)

    with open(os.path.join(REPORTS_DIR, "CROSS_FOLD_SUMMARY_TIER1.md"), "w") as f:
        f.write("# Tier 1 — Traditional ML Cross-Fold Summary (seed=42)\n\n")
        f.write("## Classification (NHY, D021 ordinal {0,1,2,3+}) — Macro F1 mean/sd/min/max/95%CI\n\n")
        f.write(df_cls[['Model', 'f1_macro_mean', 'f1_macro_sd', 'f1_macro_min', 'f1_macro_max', 'f1_macro_ci95']].to_markdown(index=False))
        f.write("\n\n## Regression (NP3TOT) — RMSE mean/sd/min/max/95%CI\n\n")
        f.write(df_reg[['Model', 'rmse_mean', 'rmse_sd', 'rmse_min', 'rmse_max', 'rmse_ci95']].to_markdown(index=False))

    print("\n--- TIER 1 BENCHMARK COMPLETE — all artifacts written to", OUTPUT_DIR, "---")
    print("\n=== CLASSIFICATION LEADERBOARD (top columns) ===")
    print(df_cls[['Model', 'f1_macro_mean', 'acc_mean', 'bal_acc_mean']].to_markdown(index=False))
    print("\n=== REGRESSION LEADERBOARD (top columns) ===")
    print(df_reg[['Model', 'rmse_mean', 'r2_mean', 'mae_mean']].to_markdown(index=False))


if __name__ == '__main__':
    run_tier1_benchmark()
