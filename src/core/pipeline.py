"""
Base Pipeline Abstraction
"""
from abc import ABC, abstractmethod

class BasePipeline(ABC):
    @abstractmethod
    def execute(self):
        pass
        
    @abstractmethod
    def validate(self):
        pass
