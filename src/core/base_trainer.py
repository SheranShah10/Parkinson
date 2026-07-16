"""
Base Trainer Abstraction
"""
from abc import ABC, abstractmethod

class BaseTrainer(ABC):
    @abstractmethod
    def train_epoch(self):
        pass
        
    @abstractmethod
    def validate_epoch(self):
        pass
        
    @abstractmethod
    def save_checkpoint(self, path: str):
        pass
