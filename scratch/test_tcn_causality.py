import torch
import torch.nn as nn
import torch.nn.functional as F

class CausalConv1d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, dilation, dropout=0.2):
        super().__init__()
        self.left_padding = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, padding=0, dilation=dilation)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        x_padded = F.pad(x, (self.left_padding, 0)) # Pad ONLY on the left (past)
        return self.dropout(self.relu(self.conv(x_padded)))

class TCN(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, kernel_size=2, dropout=0.2):
        super().__init__()
        layers = []
        in_channels = input_dim
        for i in range(num_layers):
            dilation = 2 ** i
            layers.append(CausalConv1d(in_channels, hidden_dim, kernel_size, dilation, dropout))
            in_channels = hidden_dim
        self.network = nn.Sequential(*layers)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, lengths=None):
        x = x.transpose(1, 2)
        out = self.network(x)
        out = out.transpose(1, 2)
        return out # Return full sequence for the causality test

torch.manual_seed(42)

# Create a sample sequence: 1 patient, 6 visits, 1 feature
# Shape: [Batch, Time, Features] -> [1, 6, 1]
x_original = torch.tensor([[[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]])

# Instantiate TCN
model = TCN(input_dim=1, hidden_dim=4, num_layers=3, output_dim=1, kernel_size=2, dropout=0.0) # Dropout 0 for deterministic test

# Run 1: Original Sequence
model.eval()
with torch.no_grad():
    out1 = model(x_original)

# Run 2: Modify a FUTURE timestep (Timestep 5 -> changed to 999.0)
x_modified = x_original.clone()
x_modified[0, 5, 0] = 999.0
with torch.no_grad():
    out2 = model(x_modified)

# Extract representations at T=2 (the 3rd timestep)
rep1_T2 = out1[0, 2, :]
rep2_T2 = out2[0, 2, :]

print("--- MECHANICAL CAUSALITY LEAKAGE TEST ---")
print(f"Original sequence: {x_original.squeeze().tolist()}")
print(f"Modified sequence: {x_modified.squeeze().tolist()}")
print("\nRepresentation at T=2 (Timestep 3):")
print(f"From Original: {rep1_T2.tolist()}")
print(f"From Modified: {rep2_T2.tolist()}")
print("\nRepresentation at T=5 (Timestep 6 - the modified one):")
print(f"From Original: {out1[0, 5, :].tolist()}")
print(f"From Modified: {out2[0, 5, :].tolist()}")
print("\nResult:")
if torch.allclose(rep1_T2, rep2_T2):
    print("✅ CAUSALITY PROVEN: T=2 output is IDENTICAL despite future T=5 being modified.")
else:
    print("🚨 LEAKAGE DETECTED: T=2 output changed when future T=5 was modified.")
