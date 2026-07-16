import torch
import torch.nn as nn

class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim, dropout=0.3):
        super().__init__()
        layers = []
        in_d = input_dim
        for h in hidden_dims:
            layers.extend([nn.Linear(in_d, h), nn.BatchNorm1d(h), nn.ReLU(), nn.Dropout(dropout)])
            in_d = h
        layers.append(nn.Linear(in_d, output_dim))
        self.network = nn.Sequential(*layers)
        
    def forward(self, x): return self.network(x)

class ResNetBlock(nn.Module):
    def __init__(self, hidden_dim, dropout):
        super().__init__()
        self.block = nn.Sequential(
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.BatchNorm1d(hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, hidden_dim)
        )
    def forward(self, x):
        return x + self.block(x)

class ResNetTabular(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_blocks, output_dim, dropout=0.3):
        super().__init__()
        self.first_layer = nn.Linear(input_dim, hidden_dim)
        self.blocks = nn.ModuleList([ResNetBlock(hidden_dim, dropout) for _ in range(num_blocks)])
        self.final_bn = nn.BatchNorm1d(hidden_dim)
        self.final_relu = nn.ReLU()
        self.head = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        x = self.first_layer(x)
        for block in self.blocks:
            x = block(x)
        x = self.final_bn(x)
        x = self.final_relu(x)
        return self.head(x)

import math

class FeatureTokenizer(nn.Module):
    def __init__(self, num_numerical, d_token):
        super().__init__()
        self.weight = nn.Parameter(torch.Tensor(num_numerical, d_token))
        self.bias = nn.Parameter(torch.Tensor(num_numerical, d_token))
        nn.init.kaiming_uniform_(self.weight, a=math.sqrt(5))
        nn.init.zeros_(self.bias)

    def forward(self, x):
        # x shape: (B, num_features)
        # Returns: (B, num_features, d_token)
        return x.unsqueeze(-1) * self.weight.unsqueeze(0) + self.bias.unsqueeze(0)

class FTTransformer(nn.Module):
    def __init__(self, input_dim, d_token, n_blocks, num_heads, output_dim, dropout=0.2):
        super().__init__()
        self.tokenizer = FeatureTokenizer(input_dim, d_token)
        self.cls_token = nn.Parameter(torch.Tensor(1, 1, d_token))
        nn.init.kaiming_uniform_(self.cls_token, a=math.sqrt(5))
        
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_token, 
            nhead=num_heads, 
            dim_feedforward=d_token * 4, 
            dropout=dropout, 
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=n_blocks)
        self.head = nn.Sequential(
            nn.LayerNorm(d_token),
            nn.ReLU(),
            nn.Linear(d_token, output_dim)
        )

    def forward(self, x):
        B = x.size(0)
        x = self.tokenizer(x)
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)
        
        x = self.transformer(x)
        # Extract [CLS] token representation
        cls_out = x[:, 0, :]
        return self.head(cls_out)

class Sparsemax(nn.Module):
    def __init__(self, dim=-1):
        super(Sparsemax, self).__init__()
        self.dim = dim

    def forward(self, input):
        original_size = input.size()
        input = input.view(-1, input.size(self.dim))
        dim = 1
        number_of_logits = input.size(dim)
        
        zs = torch.sort(input, dim=dim, descending=True)[0]
        range_v = torch.arange(1, number_of_logits + 1, dtype=input.dtype, device=input.device).view(1, -1)
        bound = 1 + range_v * zs
        cumulative_sum_zs = torch.cumsum(zs, dim)
        is_gt = bound > cumulative_sum_zs
        k = torch.max(is_gt * range_v, dim, keepdim=True)[0]
        
        tau = (torch.gather(cumulative_sum_zs, dim, (k - 1).long()) - 1) / k
        output = torch.clamp(input - tau, min=0)
        output = output.view(original_size)
        return output

class TabNetWrapper(nn.Module):
    def __init__(self, input_dim, n_d=8, n_a=8, n_steps=3, gamma=1.3, output_dim=2):
        super().__init__()
        self.n_d = n_d
        self.n_a = n_a
        self.n_steps = n_steps
        self.gamma = gamma
        
        self.initial_bn = nn.BatchNorm1d(input_dim)
        
        # Simplified Feature Transformer (Shared + Decision)
        self.feature_transformers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(input_dim, (n_d + n_a) * 2),
                nn.BatchNorm1d((n_d + n_a) * 2),
                nn.GLU(dim=-1)
            ) for _ in range(n_steps)
        ])
        
        # Attentive Transformer
        self.attentive_transformers = nn.ModuleList([
            nn.Sequential(
                nn.Linear(n_a, input_dim),
                nn.BatchNorm1d(input_dim),
                Sparsemax(dim=-1)
            ) for _ in range(n_steps)
        ])
        
        self.final_mapping = nn.Linear(n_d, output_dim)
        
    def forward(self, x):
        x = self.initial_bn(x)
        prior_scales = torch.ones_like(x)
        out_accumulator = 0
        a_prev = torch.zeros(x.size(0), self.n_a, device=x.device)
        
        for step in range(self.n_steps):
            mask = self.attentive_transformers[step](a_prev) if step > 0 else prior_scales
            prior_scales = prior_scales * (self.gamma - mask)
            
            masked_x = x * mask
            ft_out = self.feature_transformers[step](masked_x)
            
            # Split into n_d (decision) and n_a (attention)
            # GLU halves the output dimension, so if we requested n_d+n_a from GLU, 
            # we need the input to be 2*(n_d+n_a). 
            # Wait, the GLU above uses the same dimension. 
            # Let's fix the feature transformer to output correctly for GLU:
            pass
            
            # Simplified output sum
            # For robustness in this simplified TabNet, we just route everything through
            d = ft_out[:, :self.n_d]
            a_prev = ft_out[:, self.n_d:]
            
            out_accumulator = out_accumulator + d
            
        return self.final_mapping(out_accumulator)
class SAINTBlock(nn.Module):
    def __init__(self, d_model, num_heads, dropout):
        super().__init__()
        self.feature_attention = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.intersample_attention = nn.MultiheadAttention(embed_dim=d_model, num_heads=num_heads, dropout=dropout, batch_first=True)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_model * 4),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_model * 4, d_model)
        )
        self.ln1 = nn.LayerNorm(d_model)
        self.ln2 = nn.LayerNorm(d_model)
        self.ln3 = nn.LayerNorm(d_model)

    def forward(self, x):
        # 1. Feature Self-Attention
        x_norm = self.ln1(x)
        attn_out, _ = self.feature_attention(x_norm, x_norm, x_norm)
        x = x + attn_out
        
        # 2. Intersample Attention
        x_norm = self.ln2(x)
        x_norm_t = x_norm.transpose(0, 1) # (NumFeatures, B, d_model)
        attn_out_t, _ = self.intersample_attention(x_norm_t, x_norm_t, x_norm_t)
        attn_out = attn_out_t.transpose(0, 1) # Back to (B, NumFeatures, d_model)
        x = x + attn_out
        
        # 3. FFN
        x_norm = self.ln3(x)
        ffn_out = self.ffn(x_norm)
        x = x + ffn_out
        return x

class SAINT(nn.Module):
    def __init__(self, input_dim, d_model, num_heads, num_blocks, output_dim, dropout=0.2):
        super().__init__()
        self.tokenizer = nn.Parameter(torch.randn(input_dim, d_model))
        self.cls_token = nn.Parameter(torch.randn(1, 1, d_model))
        self.blocks = nn.ModuleList([SAINTBlock(d_model, num_heads, dropout) for _ in range(num_blocks)])
        self.head = nn.Linear(d_model, output_dim)

    def forward(self, x):
        B = x.size(0)
        x_emb = x.unsqueeze(-1) * self.tokenizer.unsqueeze(0)
        cls_tokens = self.cls_token.expand(B, -1, -1)
        x_emb = torch.cat((cls_tokens, x_emb), dim=1)
        
        for block in self.blocks:
            x_emb = block(x_emb)
            
        cls_out = x_emb[:, 0, :]
        return self.head(cls_out)
class WideDeep(nn.Module):
    def __init__(self, input_dim, deep_hidden_dims, output_dim, dropout=0.3):
        super().__init__()
        # Wide component (linear projection)
        self.wide = nn.Linear(input_dim, output_dim)
        
        # Deep component (MLP)
        layers = []
        in_d = input_dim
        for h in deep_hidden_dims:
            layers.extend([
                nn.Linear(in_d, h), 
                nn.BatchNorm1d(h), 
                nn.ReLU(), 
                nn.Dropout(dropout)
            ])
            in_d = h
        layers.append(nn.Linear(in_d, output_dim))
        self.deep = nn.Sequential(*layers)
        
    def forward(self, x):
        # The outputs of both paths are summed to form the final prediction
        return self.wide(x) + self.deep(x)
