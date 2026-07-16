import torch
import torch.nn as nn

class LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x, lengths=None):
        # x shape: [batch, time, features]
        if lengths is not None:
            # Enforce sorted=False so we don't have to pre-sort by length in the dataloader
            x = nn.utils.rnn.pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
            
        out, (hn, cn) = self.lstm(x)
        
        if lengths is not None:
            out, _ = nn.utils.rnn.pad_packed_sequence(out, batch_first=True)
            
            # Extract the actual last valid timestep for each sequence
            batch_size = out.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
            
        return self.fc(last_out)

class BiLSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout=0.2):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, bidirectional=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        
    def forward(self, x, lengths=None):
        if lengths is not None:
            x = nn.utils.rnn.pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        out, (hn, cn) = self.lstm(x)
        if lengths is not None:
            out, _ = nn.utils.rnn.pad_packed_sequence(out, batch_first=True)
            batch_size = out.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
        return self.fc(last_out)

class GRU(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, dropout=0.2):
        super().__init__()
        self.gru = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x, lengths=None):
        if lengths is not None:
            x = nn.utils.rnn.pack_padded_sequence(x, lengths, batch_first=True, enforce_sorted=False)
        out, hn = self.gru(x)
        if lengths is not None:
            out, _ = nn.utils.rnn.pad_packed_sequence(out, batch_first=True)
            batch_size = out.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
        return self.fc(last_out)

import math

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=50):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        # Handle odd d_model gracefully
        pe[:, 1::2] = torch.cos(position * div_term)[:, :pe[:, 1::2].shape[1]]
        self.register_buffer('pe', pe.unsqueeze(0)) # [1, max_len, d_model]

    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class TemporalTransformer(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, nhead=4, dropout=0.2, max_len=50):
        super().__init__()
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        self.pos_encoder = PositionalEncoding(hidden_dim, max_len)
        
        encoder_layers = nn.TransformerEncoderLayer(
            d_model=hidden_dim, 
            nhead=nhead, 
            dim_feedforward=hidden_dim*4, 
            dropout=dropout, 
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layers, num_layers)
        self.fc = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, lengths=None):
        # x shape: [batch, time, features]
        seq_len = x.size(1)
        batch_size = x.size(0)
        
        # 1. Project to d_model and add positional encoding
        x = self.input_proj(x)
        x = self.pos_encoder(x)
        
        # 2. Causal Mask (Square Subsequent Mask) -> blocks T from looking at T+1
        # PyTorch causal mask: 0 for allowed, -inf for blocked (using bool mask is also standard)
        causal_mask = nn.Transformer.generate_square_subsequent_mask(seq_len).to(x.device)
        
        # 3. Padding Mask -> blocks attention to padded zeroes
        padding_mask = None
        if lengths is not None:
            # True means "ignore this position"
            padding_mask = torch.arange(seq_len).expand(batch_size, seq_len).to(lengths.device) >= lengths.unsqueeze(1)
            
        # 4. Transformer Pass
        out = self.transformer_encoder(x, mask=causal_mask, src_key_padding_mask=padding_mask, is_causal=True)
        
        # 5. Extract final timestep
        if lengths is not None:
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
            
        return self.fc(last_out)
import torch.nn.functional as F

class CausalConv1d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size, dilation, dropout=0.2):
        super().__init__()
        self.left_padding = (kernel_size - 1) * dilation
        self.conv = nn.Conv1d(in_channels, out_channels, kernel_size, padding=0, dilation=dilation)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        # x shape: [batch, features, time]
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
        # x comes in as [batch, time, features] -> transpose to [batch, features, time] for Conv1d
        x = x.transpose(1, 2)
        out = self.network(x)
        # out is [batch, hidden_dim, time] -> transpose back to [batch, time, hidden_dim]
        out = out.transpose(1, 2)
        
        if lengths is not None:
            # Extract the output at the true final timestep for each sequence
            batch_size = out.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out.size(2)).unsqueeze(1)
            last_out = out.gather(1, idx).squeeze(1)
        else:
            last_out = out[:, -1, :]
            
        return self.fc(last_out)

class CNN_LSTM(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim, kernel_size=2, dropout=0.2):
        super().__init__()
        # CNN Feature Extractor (Strictly Causal)
        self.cnn = CausalConv1d(input_dim, hidden_dim, kernel_size=kernel_size, dilation=1, dropout=dropout)
        
        # LSTM Sequence Processor
        self.lstm = nn.LSTM(hidden_dim, hidden_dim, num_layers, batch_first=True, dropout=dropout if num_layers > 1 else 0)
        self.fc = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x, lengths=None):
        # 1. CNN Pass (Requires [Batch, Features, Time])
        x_cnn = x.transpose(1, 2)
        out_cnn = self.cnn(x_cnn)
        # Transpose back to [Batch, Time, Features] for LSTM
        out_cnn = out_cnn.transpose(1, 2)
        
        # 2. LSTM Pass
        if lengths is not None:
            out_cnn = torch.nn.utils.rnn.pack_padded_sequence(out_cnn, lengths, batch_first=True, enforce_sorted=False)
            
        out_lstm, (hn, cn) = self.lstm(out_cnn)
        
        if lengths is not None:
            out_lstm, _ = torch.nn.utils.rnn.pad_packed_sequence(out_lstm, batch_first=True)
            batch_size = out_lstm.size(0)
            idx = (lengths - 1).view(-1, 1).expand(batch_size, out_lstm.size(2)).unsqueeze(1)
            last_out = out_lstm.gather(1, idx).squeeze(1)
        else:
            last_out = out_lstm[:, -1, :]
            
        return self.fc(last_out)
