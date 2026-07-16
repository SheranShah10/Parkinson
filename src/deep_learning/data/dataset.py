import torch
from torch.utils.data import Dataset

class ParkinsonTabularDataset(Dataset):
    def __init__(self, X, y, task_type="classification"):
        self.X = torch.tensor(X.values, dtype=torch.float32)
        if task_type == "classification":
            self.y = torch.tensor(y.values, dtype=torch.long)
        else:
            self.y = torch.tensor(y.values, dtype=torch.float32)

    def __len__(self): return len(self.X)
    
    def __getitem__(self, idx): return self.X[idx], self.y[idx]
