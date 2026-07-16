"""
Base Model Abstraction
"""
from abc import ABC, abstractmethod

class BaseModel(ABC):
    @abstractmethod
    def build_model(self):
        """Constructs the model architecture."""
        pass
        
    @abstractmethod
    def forward(self, x):
        """Forward pass of the model."""
        pass
        
    def get_parameter_count(self) -> int:
        """Returns total trainable parameters. Must be overridden if using PyTorch."""
        return 0
