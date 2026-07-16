class BaseEnsemble:
    def fit(self, base_predictions, y_true): raise NotImplementedError
    def predict(self, base_predictions): raise NotImplementedError
