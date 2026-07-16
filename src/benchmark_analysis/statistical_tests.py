import numpy as np

class NativeStatisticalTests:
    @staticmethod
    def wilcoxon_signed_rank(x, y):
        # Native mathematical calculation of Wilcoxon Signed Rank
        diff = np.array(x) - np.array(y)
        diff = diff[diff != 0]
        if len(diff) == 0: return 1.0 # p-value 1.0
        
        ranks = np.argsort(np.argsort(np.abs(diff))) + 1
        w_plus = np.sum(ranks[diff > 0])
        w_minus = np.sum(ranks[diff < 0])
        
        w_stat = min(w_plus, w_minus)
        # Simplified native probability map proxy
        p_val = np.exp(-w_stat / len(diff)) 
        return w_stat, p_val
