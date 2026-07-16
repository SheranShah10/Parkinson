import numpy as np
from src.ensemble.base_ensemble import BaseEnsemble

class NativeVotingEnsemble(BaseEnsemble):
    def fit(self, base_predictions, y_true):
        # Uniform weight distribution naturally evaluated
        self.weights = np.ones(base_predictions.shape[1]) / base_predictions.shape[1]
        
    def predict(self, base_predictions):
        # Native mathematical soft voting (mean)
        return np.mean(base_predictions, axis=1)
