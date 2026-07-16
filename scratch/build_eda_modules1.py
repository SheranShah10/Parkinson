import os

src_eda = "C:/Users/Sheran/Desktop/Parkinson/src/eda"
os.makedirs(src_eda, exist_ok=True)

with open(os.path.join(src_eda, '__init__.py'), 'w') as f:
    f.write("")

# 1. leakage_detector.py
with open(os.path.join(src_eda, 'leakage_detector.py'), 'w') as f:
    f.write("""import pandas as pd
import numpy as np
import os

def detect_leakage(df, reports_dir):
    print("Detecting Target Leakage...")
    targets = [c for c in df.columns if c.startswith('TARGET_')]
    identifiers = ['PATNO', 'EVENT_ID', 'INFODT']
    
    leakage_report = [
        "# Target Leakage Detection Report\\n",
        "## Identifier Leakage",
        "The following variables are strict identifiers and must NOT be used as predictors:"
    ]
    for i in identifiers:
        if i in df.columns:
            leakage_report.append(f"- {i}")
            
    leakage_report.append("\\n## High Correlation Leakage (>0.99)")
    leakage_report.append("The following features exhibit >0.99 correlation with targets and represent potential leakage:")
    
    # Calculate correlations efficiently
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    numeric_cols = [c for c in numeric_cols if c not in targets + identifiers]
    
    found_leakage = False
    for t in targets:
        if t not in df.columns or df[t].dtype not in [np.float64, np.int64, float, int]: continue
        y = df[t].values
        mask_y = ~np.isnan(y)
        for c in numeric_cols:
            x = df[c].values
            mask_x = ~np.isnan(x)
            mask = mask_y & mask_x
            if mask.sum() > 10:
                corr = np.corrcoef(x[mask], y[mask])[0, 1]
                if abs(corr) > 0.99:
                    leakage_report.append(f"- **{c}** correlates with {t} ({corr:.4f})")
                    found_leakage = True
                    
    if not found_leakage:
        leakage_report.append("No features exceeded the 0.99 correlation threshold.")
        
    leakage_report.append("\\n## Future-Derived Variables")
    leakage_report.append("Variables containing 'DELTA', 'CHANGE', or derived targets from future dates must be excluded during cross-sectional prediction tasks.")
    
    with open(os.path.join(reports_dir, 'leakage_report.md'), 'w', encoding='utf-8') as f:
        f.write("\\n".join(leakage_report))
""")

# 2. feature_stability.py
with open(os.path.join(src_eda, 'feature_stability.py'), 'w') as f:
    f.write("""import pandas as pd
import numpy as np
import os

def analyze_stability(df, reports_dir):
    print("Analyzing Feature Stability...")
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    num_cols = [c for c in num_cols if c not in ['PATNO'] and not c.startswith('TARGET_')]
    
    results = []
    for c in num_cols:
        col_mean = df[c].mean()
        col_var = df[c].var()
        cv = np.sqrt(col_var) / abs(col_mean) if col_mean != 0 else np.nan
        
        # Shift analysis
        if 'EVENT_ID' in df.columns:
            bl = df[df['EVENT_ID'] == 'BL'][c].mean()
            v04 = df[df['EVENT_ID'] == 'V04'][c].mean()
            shift = (v04 - bl) / abs(bl) if bl != 0 and not np.isnan(bl) and not np.isnan(v04) else np.nan
        else:
            shift = np.nan
            
        results.append({
            'Feature': c,
            'Overall_Mean': col_mean,
            'Temporal_Variance': col_var,
            'Coefficient_of_Variation': cv,
            'Baseline_vs_V04_Shift': shift
        })
        
    df_res = pd.DataFrame(results)
    df_res.to_csv(os.path.join(reports_dir, 'feature_stability.csv'), index=False)
    
    report = [
        "# Feature Stability Report\\n",
        "## Summary",
        f"- Total features analyzed: {len(num_cols)}",
        f"- Features with zero variance: {df_res['Temporal_Variance'].eq(0).sum()}",
        f"- Median Coefficient of Variation: {df_res['Coefficient_of_Variation'].median():.4f}",
        "\\nDetailed stability metrics have been saved to `feature_stability.csv`."
    ]
    with open(os.path.join(reports_dir, 'feature_stability_report.md'), 'w', encoding='utf-8') as f:
        f.write("\\n".join(report))
""")

# 3. patient_similarity.py
with open(os.path.join(src_eda, 'patient_similarity.py'), 'w') as f:
    f.write("""import pandas as pd
import numpy as np
import os

def compute_similarity(df, reports_dir):
    print("Computing Patient Similarity...")
    # Isolate baseline
    df_bl = df[df['EVENT_ID'] == 'BL'].copy() if 'EVENT_ID' in df.columns else df.copy()
    if len(df_bl) == 0: df_bl = df.copy()
    
    num_cols = df_bl.select_dtypes(include=np.number).columns.tolist()
    # Take a core subset to prevent memory explosion
    num_cols = [c for c in num_cols if c not in ['PATNO'] and not c.startswith('TARGET_')]
    
    # Simple imputation for core
    core = df_bl[num_cols].fillna(df_bl[num_cols].median()).values
    
    # Scale
    core_scaled = (core - np.mean(core, axis=0)) / (np.std(core, axis=0) + 1e-10)
    
    # Cosine similarity matrix (approx)
    dot = np.dot(core_scaled, core_scaled.T)
    norms = np.linalg.norm(core_scaled, axis=1)
    cos_sim = dot / (np.outer(norms, norms) + 1e-10)
    
    # NN dist
    np.fill_diagonal(cos_sim, -1)
    nn_sim = np.max(cos_sim, axis=1)
    
    report = [
        "# Patient Similarity Analysis\\n",
        "This analysis supports future Graph Neural Network (GNN) topology construction by evaluating patient-to-patient distances in the multidimensional clinical space.",
        "## Cosine Similarity Metrics (Baseline)",
        f"- Mean Nearest-Neighbor Similarity: {np.mean(nn_sim):.4f}",
        f"- Max Nearest-Neighbor Similarity: {np.max(nn_sim):.4f}",
        f"- Min Nearest-Neighbor Similarity: {np.min(nn_sim):.4f}",
        "\\n## Clustering Implications",
        "High average NN similarities suggest dense sub-manifolds (clusters), ideal for GNN edge weights."
    ]
    with open(os.path.join(reports_dir, 'patient_similarity_analysis.md'), 'w', encoding='utf-8') as f:
        f.write("\\n".join(report))
""")

# 4. modality_overlap.py
with open(os.path.join(src_eda, 'modality_overlap.py'), 'w') as f:
    f.write("""import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_overlap(df, reports_dir, figures_dir):
    print("Analyzing Modality Overlap...")
    
    mods = {
        "Clinical": ["NP1RTOT", "NP2PTOT", "clini_"],
        "Motor": ["NP3TOT", "MDS-U_NP3TOT"],
        "Imaging": ["Dopam_", "Xing_"],
        "Proteomics": ["Kinet_", "Curre_", "SAA_B"],
        "Smartphone": ["Roche_count"]
    }
    
    presence = {}
    for mod, prefixes in mods.items():
        cols = [c for c in df.columns if any(p in c for p in prefixes)]
        if cols:
            presence[mod] = df[cols].notnull().any(axis=1).astype(int)
        else:
            presence[mod] = np.zeros(len(df))
            
    df_pres = pd.DataFrame(presence)
    
    # Overlap matrix (count of visits having both)
    overlap = df_pres.T.dot(df_pres)
    overlap.to_csv(os.path.join(reports_dir, 'modality_overlap_matrix.csv'))
    
    # Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(overlap, annot=True, fmt='d', cmap='Blues')
    plt.title("Modality Overlap Matrix (Shared Visits)")
    plt.savefig(os.path.join(figures_dir, 'modality_overlap_heatmap.png'), dpi=300, bbox_inches='tight')
    plt.close()
""")
