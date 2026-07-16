class BaseExplainer:
    def explain_global(self, model, X): raise NotImplementedError
    def explain_local(self, model, X, instance_idx): raise NotImplementedError
