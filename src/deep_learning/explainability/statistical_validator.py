import numpy as np
from scipy.stats import spearmanr, kendalltau

class StatisticalValidator:
    @staticmethod
    def compute_rank_correlations(attributions_1, attributions_2):
        """
        Computes real Spearman and Kendall Tau correlations between two attribution arrays.
        Useful for comparing XAI methods (e.g. SHAP vs Captum) or Fold 1 vs Fold 2 stability.
        """
        # Flatten in case of multi-dimensional tensors
        flat_1 = np.asarray(attributions_1).flatten()
        flat_2 = np.asarray(attributions_2).flatten()
        
        # Calculate real statistics
        spearman_corr, spearman_p = spearmanr(flat_1, flat_2)
        kendall_corr, kendall_p = kendalltau(flat_1, flat_2)
        
        return {
            "Spearman": float(spearman_corr),
            "Spearman_P_Value": float(spearman_p),
            "Kendall_Tau": float(kendall_corr),
            "Kendall_P_Value": float(kendall_p)
        }

    @staticmethod
    def compute_fold_stability(fold_attributions_list):
        """
        Calculates fold-to-fold variance and Attribution Agreement Score.
        fold_attributions_list: List of numpy arrays, each representing feature attributions for a fold.
        """
        stacked = np.stack(fold_attributions_list, axis=0) # Shape: (Num_Folds, Num_Features)
        
        # Calculate Variance per feature across folds
        variances = np.var(stacked, axis=0)
        mean_variance = float(np.mean(variances))
        
        # Calculate Attribution Agreement Score
        # Flawed variance normalizations collapse toward 1.0. 
        # A rigorous agreement metric is the Mean Pairwise Rank Correlation across all folds.
        num_folds = len(fold_attributions_list)
        spearmans = []
        for i in range(num_folds):
            for j in range(i + 1, num_folds):
                flat_i = np.asarray(fold_attributions_list[i]).flatten()
                flat_j = np.asarray(fold_attributions_list[j]).flatten()
                corr, _ = spearmanr(flat_i, flat_j)
                spearmans.append(corr)
                
        agreement_score = float(np.mean(spearmans)) if spearmans else 0.0
            
        return {
            "Mean_Feature_Variance_Across_Folds": mean_variance,
            "Attribution_Agreement_Score": float(agreement_score)
        }
