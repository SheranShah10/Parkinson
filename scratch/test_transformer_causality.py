import torch
import torch.nn as nn
import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=50):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)[:, :pe[:, 1::2].shape[1]]
        self.register_buffer('pe', pe.unsqueeze(0)) 

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class TransformerEncoderCausalTest(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=4, num_layers=2, nhead=2, max_len=10):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        self.pos_encoder = PositionalEncoding(hidden_dim, max_len)
        encoder_layers = nn.TransformerEncoderLayer(
            d_model=hidden_dim, nhead=nhead, dim_feedforward=16, dropout=0.0, batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)

    def forward(self, x):
        seq_len = x.size(1)
        x = self.input_proj(x)
        x = self.pos_encoder(x)
        
        # STRICT CAUSAL MASK
        causal_mask = nn.Transformer.generate_square_subsequent_mask(seq_len).to(x.device)
        
        # Return the full sequence out of the encoder to inspect T=2 vs T=5
        out = self.transformer_encoder(x, mask=causal_mask, is_causal=True)
        return out

torch.manual_seed(42)

# Create a sample sequence: 1 patient, 6 visits, 1 feature
x_original = torch.tensor([[[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]])
model = TransformerEncoderCausalTest()
model.eval()

# Run 1: Original
with torch.no_grad():
    out1 = model(x_original)

# Run 2: Modify Future
x_modified = x_original.clone()
x_modified[0, 5, 0] = 999.0
with torch.no_grad():
    out2 = model(x_modified)

rep1_T2 = out1[0, 2, :]
rep2_T2 = out2[0, 2, :]

print("--- MECHANICAL CAUSALITY LEAKAGE TEST (TRANSFORMER) ---")
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
    print("CAUSALITY PROVEN: T=2 output is IDENTICAL despite future T=5 being modified.")
else:
    print("LEAKAGE DETECTED: T=2 output changed when future T=5 was modified.")
