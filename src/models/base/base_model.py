class BaseModelInterface:
    def initialize(self, config): raise NotImplementedError
    def fit(self, X, y): raise NotImplementedError
    def predict(self, X): raise NotImplementedError
    def predict_proba(self, X): raise NotImplementedError
    def save(self, path): raise NotImplementedError
    def load(self, path): raise NotImplementedError
    def export_metadata(self): return {}
