"""
Tier 1: Traditional Machine Learning Benchmark (v5 — Final Suite 14/12 Models)
PPMI DaTSCAN — Parkinson's severity (NP3TOT) & stage (NHY)
"""

!pip install xgboost lightgbm catboost scikit-learn -q

import os
import sys
import time
import warnings
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GroupKFold, StratifiedGroupKFold
from sklearn.metrics import (
    accuracy_score, balanced_accuracy_score, f1_score, precision_score, recall_score,
    mean_squared_error, mean_absolute_error, r2_score
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

def collapse_nhy(raw_values):
    mapped = np.full(raw_values.shape, np.nan)
    valid = ~np.isnan(raw_values)
    v = raw_values[valid]
    out = np.select([v == 0, v == 1, v == 2, v >= 3], [0, 1, 2, 3], default=np.nan)
    mapped[valid] = out
    return mapped

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

    y_cls = collapse_nhy(df['NHY'].values.astype(float))
    y_reg = df['NP3TOT'].values
    groups = df['PATNO'].values

    # SURGICAL LEAKAGE PURGE (Tested and Confirmed)
    leaky_patterns = ['NHY', 'NP3', 'TARGET_', 'MOTOR_SEVERITY', 'TEMPORAL_MOTOR_SLOPE', 'PD_DX', 'CLINI_', 'MDS-U_'] 
    leaky_cols = [c for c in df.columns if any(pat in c.upper() for pat in leaky_patterns)]
    df_features = df.drop(columns=leaky_cols + ['PATNO', 'EVENT_ID'], errors='ignore')

    # Drop 100% missing or zero-variance columns BEFORE returning
    missing_mask = df_features.isnull().mean() == 1.0
    df_features = df_features.loc[:, ~missing_mask]
    
    nunique = df_features.nunique(dropna=True)
    df_features = df_features.drop(columns=nunique[nunique <= 1].index.tolist())

    numeric_cols = df_features.select_dtypes(include=[np.number]).columns
    df_features = df_features[numeric_cols]
    
    feature_names = df_features.columns.tolist()
    X = df_features.values

    return X, y_cls, y_reg, groups, feature_names

def get_stats(fold_metrics):
    arr = np.array([x for x in fold_metrics if x is not None and not np.isnan(x)], dtype=float)
    if len(arr) == 0: return dict(mean=np.nan)
    return dict(mean=arr.mean())

def _flatten_stats(metrics_dict):
    row = {}
    for key, values in metrics_dict.items():
        row[f"{key}_mean"] = get_stats(values)['mean']
    return row

def evaluate_classification(models, X, y, groups):
    results = []
    sgkf = StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=SEED)
    valid_idx = ~np.isnan(y)
    X_valid, y_valid, groups_valid = X[valid_idx], y[valid_idx], groups[valid_idx]

    for name, model in models.items():
        print(f"  > Training Classification: {name}...")
        metrics = {k: [] for k in ['acc', 'bal_acc', 'f1_macro']}
        for train_idx, val_idx in sgkf.split(X_valid, y_valid, groups_valid):
            X_train, y_train = X_valid[train_idx], y_valid[train_idx]
            X_val, y_val = X_valid[val_idx], y_valid[val_idx]

            imputer, scaler = SimpleImputer(strategy='median'), StandardScaler()
            X_train = scaler.fit_transform(imputer.fit_transform(X_train))
            X_val = scaler.transform(imputer.transform(X_val))

            model.fit(X_train, y_train)
            preds = model.predict(X_val)

            metrics['acc'].append(accuracy_score(y_val, preds))
            metrics['bal_acc'].append(balanced_accuracy_score(y_val, preds))
            metrics['f1_macro'].append(f1_score(y_val, preds, average='macro'))

        row = {'Model': name}
        row.update(_flatten_stats(metrics))
        results.append(row)

    return pd.DataFrame(results)

def evaluate_regression(models, X, y, groups):
    results = []
    gkf = GroupKFold(n_splits=5)
    valid_idx = ~np.isnan(y)
    X_valid, y_valid, groups_valid = X[valid_idx], y[valid_idx], groups[valid_idx]

    for name, model in models.items():
        print(f"  > Training Regression: {name}...")
        metrics = {k: [] for k in ['rmse', 'mae', 'r2']}
        for train_idx, val_idx in gkf.split(X_valid, y_valid, groups_valid):
            X_train, y_train = X_valid[train_idx], y_valid[train_idx]
            X_val, y_val = X_valid[val_idx], y_valid[val_idx]

            imputer, scaler = SimpleImputer(strategy='median'), StandardScaler()
            X_train = scaler.fit_transform(imputer.fit_transform(X_train))
            X_val = scaler.transform(imputer.transform(X_val))

            model.fit(X_train, y_train)
            preds = model.predict(X_val)

            metrics['rmse'].append(np.sqrt(mean_squared_error(y_val, preds)))
            metrics['mae'].append(mean_absolute_error(y_val, preds))
            metrics['r2'].append(r2_score(y_val, preds))

        row = {'Model': name}
        row.update(_flatten_stats(metrics))
        results.append(row)

    return pd.DataFrame(results)

def run_tier1_benchmark():
    print("Loading Data & Running Quality Gates...")
    X, y_cls, y_reg, groups, feature_names = get_data()

    # THE FULL 14 CLASSIFICATION MODELS
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
        'Support Vector Machine (RBF)': SVC(random_state=SEED),
        'K-Nearest Neighbors': KNeighborsClassifier(),
        'Gaussian Naive Bayes': GaussianNB(),
        'MLPClassifier': MLPClassifier(max_iter=1000, random_state=SEED)
    }

    # THE FULL 12 REGRESSION MODELS
    reg_models = {
        'Linear Regression': LinearRegression(),
        'Ridge Regression': Ridge(random_state=SEED),
        'Lasso Regression': Lasso(random_state=SEED),
        'ElasticNet': ElasticNet(random_state=SEED),
        'Random Forest Regressor': RandomForestRegressor(n_jobs=-1, random_state=SEED),
        'Extra Trees Regressor': ExtraTreesRegressor(n_jobs=-1, random_state=SEED),
        'Gradient Boosting Regressor': GradientBoostingRegressor(random_state=SEED),
        'HistGradientBoostingRegressor': HistGradientBoostingRegressor(random_state=SEED),
        'XGBoost Regressor': XGBRegressor(n_jobs=-1, random_state=SEED),
        'LightGBM Regressor': LGBMRegressor(n_jobs=-1, verbose=-1, random_state=SEED),
        'CatBoost Regressor': CatBoostRegressor(verbose=0, thread_count=-1, random_state=SEED),
        'Support Vector Regressor (SVR)': SVR()
    }

    print("\n--- RUNNING TIER 1 CLASSIFICATION ---")
    df_cls = evaluate_classification(clf_models, X, y_cls, groups)
    df_cls = df_cls.sort_values('f1_macro_mean', ascending=False)
    
    print("\n--- RUNNING TIER 1 REGRESSION ---")
    df_reg = evaluate_regression(reg_models, X, y_reg, groups)
    df_reg = df_reg.sort_values('rmse_mean', ascending=True)
    
    print("\n--- TIER 1 BENCHMARK COMPLETE ---")
    print("\n=== CLASSIFICATION LEADERBOARD ===")
    print(df_cls.to_markdown(index=False))
    print("\n=== REGRESSION LEADERBOARD ===")
    print(df_reg.to_markdown(index=False))

if __name__ == '__main__':
    run_tier1_benchmark()
