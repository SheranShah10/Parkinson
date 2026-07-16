import pandas as pd
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
        "# Patient Similarity Analysis\n",
        "This analysis supports future Graph Neural Network (GNN) topology construction by evaluating patient-to-patient distances in the multidimensional clinical space.",
        "## Cosine Similarity Metrics (Baseline)",
        f"- Mean Nearest-Neighbor Similarity: {np.mean(nn_sim):.4f}",
        f"- Max Nearest-Neighbor Similarity: {np.max(nn_sim):.4f}",
        f"- Min Nearest-Neighbor Similarity: {np.min(nn_sim):.4f}",
        "\n## Clustering Implications",
        "High average NN similarities suggest dense sub-manifolds (clusters), ideal for GNN edge weights."
    ]
    with open(os.path.join(reports_dir, 'patient_similarity_analysis.md'), 'w', encoding='utf-8') as f:
        f.write("\n".join(report))
