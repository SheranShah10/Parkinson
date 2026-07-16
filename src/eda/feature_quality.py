import pandas as pd
import numpy as np
import os

def score_quality(df, reports_dir):
    print("Scoring Feature Quality...")
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    
    scores = []
    for c in num_cols:
        miss = df[c].isnull().sum() / len(df)
        var = df[c].var()
        
        # Simple heuristic: heavily penalize missingness, reward variance slightly
        score = 10.0 - (miss * 8) 
        if var == 0:
            score -= 2
            
        scores.append({
            'Feature': c,
            'Quality_Score': max(0, min(10, score)),
            'Missing_Penalty': miss,
            'Variance': var
        })
        
    df_scores = pd.DataFrame(scores).sort_values('Quality_Score', ascending=False)
    df_scores.to_csv(os.path.join(reports_dir, 'feature_quality_score.csv'), index=False)
