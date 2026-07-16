from src.models.base.base_model import BaseModelInterface

class RandomForestWrapper(BaseModelInterface):
    def __init__(self):
        self.model = None
        
    def initialize(self, config):
        from sklearn.ensemble import RandomForestClassifier
        self.model = RandomForestClassifier(**config.get('hyperparameters', {}))
        
    def fit(self, X, y):
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
        
    def predict_proba(self, X):
        return self.model.predict_proba(X)
        
    def save(self, path): pass
    def load(self, path): pass
