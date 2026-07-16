from src.explainability.base_explainer import BaseExplainer

class SHAPExplainer(BaseExplainer):
    def explain_global(self, model, X):
        import shap # Will trigger authentic ImportError
        explainer = shap.TreeExplainer(model)
        return explainer.shap_values(X)
        
    def explain_local(self, model, X, instance_idx):
        import shap
        explainer = shap.Explainer(model)
        return explainer(X[instance_idx:instance_idx+1])
