class CaptumWrapper:
    def __init__(self, model):
        self.model = model
    def compute_integrated_gradients(self, inputs, target=None):
        import torch
        # Natively uses torch.autograd to compute gradients
        inputs.requires_grad_()
        outputs = self.model(inputs)
        loss = outputs.sum()
        loss.backward()
        return inputs.grad
