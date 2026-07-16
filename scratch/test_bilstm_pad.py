import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

# Dummy Data: 1 patient, max length 6, feature dim 1
# Patient has 3 real visits (all 1.0), and 3 padded visits (all 0.0)
x = torch.tensor([[[1.0], [1.0], [1.0], [0.0], [0.0], [0.0]]])
lengths = torch.tensor([3])

# BiLSTM with weights set to 1 and bias to 0 to make math obvious
lstm = nn.LSTM(input_size=1, hidden_size=1, batch_first=True, bidirectional=True)
with torch.no_grad():
    for name, param in lstm.named_parameters():
        if 'weight' in name: nn.init.ones_(param)
        elif 'bias' in name: nn.init.zeros_(param)

# Pass WITH packing (RIGHT WAY - ignores padding)
x_packed = pack_padded_sequence(x, lengths, batch_first=True)
out_packed, _ = lstm(x_packed)
out_unpacked_again, _ = pad_packed_sequence(out_packed, batch_first=True)
print(f"Packed Backward Pass state at T=3 (True End): {out_unpacked_again[0, 2, 1].item():.4f}")
print(f"Packed Backward Pass state at T=6 (Padding): {out_unpacked_again[0, 5, 1].item():.4f}")
