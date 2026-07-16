import numpy as np
from src.explainability.base_explainer import BaseExplainer

class NativePermutationExplainer(BaseExplainer):
    def explain_global(self, model, X, y_true, eval_func, n_repeats=5):
        # Native, authentic ML evaluation logic
        baseline_score = eval_func(y_true, model.predict(X))
        importances = []
        for col_idx in range(X.shape[1]):
            col_scores = []
            for _ in range(n_repeats):
                X_permuted = X.copy()
                np.random.shuffle(X_permuted[:, col_idx])
                score = eval_func(y_true, model.predict(X_permuted))
                col_scores.append(baseline_score - score)
            importances.append(np.mean(col_scores))
        return np.array(importances)
