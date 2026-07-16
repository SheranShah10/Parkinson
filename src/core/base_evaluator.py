"""
Base Evaluator Abstraction
"""
from abc import ABC, abstractmethod

class BaseEvaluator(ABC):
    @abstractmethod
    def evaluate(self, predictions, targets):
        pass
