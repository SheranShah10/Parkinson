import os

base_dir = "C:/Users/Sheran/Desktop/Parkinson"
dirs = [
    "configs/models/ml",
    "src/machine_learning/classification",
    "src/machine_learning/regression",
    "src/machine_learning/trainers",
    "src/machine_learning/evaluators",
    "src/machine_learning/predictors",
    "src/machine_learning/factories",
    "src/machine_learning/utils",
    "src/utils",
    "reports/figures/ml"
]

for d in dirs:
    os.makedirs(os.path.join(base_dir, d), exist_ok=True)
    if d.startswith("src/"):
        with open(os.path.join(base_dir, d, "__init__.py"), "w") as f: f.write("")

# 1. Dependency Manager
dep_code = """import importlib

class DependencyManager:
    @staticmethod
    def check_dependency(module_name):
        try:
            importlib.import_module(module_name)
            return True, "Available"
        except ImportError as e:
            return False, str(e)
            
    @staticmethod
    def validate_environment():
        dependencies = ['sklearn', 'lightgbm', 'xgboost', 'catboost', 'matplotlib', 'seaborn', 'shap', 'optuna']
        report = {}
        for dep in dependencies:
            is_avail, msg = DependencyManager.check_dependency(dep)
            report[dep] = {"Available": is_avail, "Message": msg}
        return report
"""
with open(os.path.join(base_dir, "src/utils/dependency_manager.py"), "w") as f: f.write(dep_code)

# 2. Authentic Model Wrappers (Classification)
rf_code = """from src.models.base.base_model import BaseModelInterface

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
"""
with open(os.path.join(base_dir, "src/machine_learning/classification/rf_wrapper.py"), "w") as f: f.write(rf_code)

xgb_code = """from src.models.base.base_model import BaseModelInterface

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
"""
with open(os.path.join(base_dir, "src/machine_learning/classification/xgb_wrapper.py"), "w") as f: f.write(xgb_code)


