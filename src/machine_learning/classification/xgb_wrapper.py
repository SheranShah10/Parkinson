from src.models.base.base_model import BaseModelInterface

class XGBoostWrapper(BaseModelInterface):
    def __init__(self):
        self.model = None
        
    def initialize(self, config):
        import xgboost as xgb
        self.model = xgb.XGBClassifier(**config.get('hyperparameters', {}))
        
    def fit(self, X, y):
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
        
    def predict_proba(self, X):
        return self.model.predict_proba(X)
        
    def save(self, path): pass
    def load(self, path): pass
