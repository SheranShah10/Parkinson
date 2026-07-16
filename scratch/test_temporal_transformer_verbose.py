import torch
import torch.nn as nn
import math

class TemporalTransformerModel(nn.Module):
    def __init__(self, input_dim=1, hidden_dim=4, num_layers=2, nhead=2, max_len=10):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        self.temporal_embedding = nn.Embedding(max_len, hidden_dim)
        encoder_layers = nn.TransformerEncoderLayer(hidden_dim, nhead, 16, 0.0, batch_first=True)
        self.transformer = nn.TransformerEncoder(encoder_layers, num_layers)

    def forward(self, x, lengths=None):
        seq_len, batch_size = x.size(1), x.size(0)
        positions = torch.arange(0, seq_len, dtype=torch.long, device=x.device).unsqueeze(0).expand(batch_size, seq_len)
        x = self.input_proj(x) + self.temporal_embedding(positions)
        
        causal_mask = torch.triu(torch.ones(seq_len, seq_len, dtype=torch.bool, device=x.device), diagonal=1)
        
        padding_mask = None
        if lengths is not None:
            padding_mask = torch.arange(seq_len).expand(batch_size, seq_len).to(lengths.device) >= lengths.unsqueeze(1)
            
        out = self.transformer(x, mask=causal_mask, src_key_padding_mask=padding_mask, is_causal=True)
        return out

def run_test():
    name = "TEMPORAL TRANSFORMER"
    print(f"\n{'='*50}\n--- MECHANICAL CAUSALITY LEAKAGE TEST: {name} ---\n{'='*50}")
    x_original = torch.tensor([[[1.0], [2.0], [3.0], [4.0], [5.0], [6.0]]])
    
    torch.manual_seed(42)
    model = TemporalTransformerModel()
    model.eval()

    with torch.no_grad():
        out1 = model(x_original)

    x_modified = x_original.clone()
    x_modified[0, 5, 0] = 999.0
    with torch.no_grad():
        out2 = model(x_modified)

    rep1_T2 = out1[0, 2, :]
    rep2_T2 = out2[0, 2, :]
    
    print(f"Representation at T=2 (Timestep 3):")
    print(f"  From Original: {rep1_T2.tolist()}")
    print(f"  From Modified: {rep2_T2.tolist()}")
    
    print(f"\nRepresentation at T=5 (Timestep 6 - the mutated one):")
    print(f"  From Original: {out1[0, 5, :].tolist()}")
    print(f"  From Modified: {out2[0, 5, :].tolist()}")

    if torch.allclose(rep1_T2, rep2_T2):
        print(f"\nCAUSALITY PROVEN ({name}): T=2 output is mathematically IDENTICAL despite future T=5 being mutated.")
    else:
        print(f"\nLEAKAGE DETECTED ({name}): T=2 output changed when future T=5 was modified.")

run_test()
