class ExplainabilityManager:
    def __init__(self, model, architecture_type):
        self.model = model
        self.arch_type = architecture_type

    def dispatch_explanation(self, inputs):
        if self.arch_type in ["MLP", "ResNet"]:
            from src.deep_learning.explainability.captum_wrapper import CaptumWrapper
            explainer = CaptumWrapper(self.model)
            return explainer.compute_integrated_gradients(inputs)
        return None
