import pandas as pd
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
