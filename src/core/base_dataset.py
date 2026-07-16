"""
Base Dataset Abstraction
"""
from abc import ABC, abstractmethod

class BaseDataset(ABC):
    @abstractmethod
    def __len__(self):
        pass
        
    @abstractmethod
    def __getitem__(self, idx):
        pass
        
    @abstractmethod
    def collate_fn(self, batch):
        pass
