"""
Core Registry
"""
from typing import Dict, Any, Callable

class Registry:
    def __init__(self, name: str):
        self._name = name
        self._module_dict: Dict[str, Any] = {}
        
    def register(self, name: str = None) -> Callable:
        def _register(cls):
            key = name if name is not None else cls.__name__
            if key in self._module_dict:
                raise KeyError(f"{key} is already registered in {self._name}")
            self._module_dict[key] = cls
            return cls
        return _register
        
    def get(self, name: str) -> Any:
        if name not in self._module_dict:
            raise KeyError(f"{name} is not registered in {self._name}")
        return self._module_dict[name]

MODELS = Registry("models")
DATASETS = Registry("datasets")
OPTIMIZERS = Registry("optimizers")
SCHEDULERS = Registry("schedulers")
PIPELINES = Registry("pipelines")
