import torch
import torch.nn as nn

class SSM_MambaBlock(nn.Module):
    """
    Minimal PyTorch implementation of a State Space Model (SSM) block 
    inspired by Mamba architecture for low-latency sequence modeling.
    This serves as a high-performance, linear-time alternative to 
    traditional Multi-Head Attention (MHA).
    """
    def __init__(self, d_model, d_state=16, d_conv=4, expand=2):
        super().__init__()
        self.d_model = d_model
        self.d_state = d_state
        self.d_conv = d_conv
        self.expand = expand
        self.d_inner = int(self.expand * self.d_model)

        self.in_proj = nn.Linear(self.d_model, self.d_inner * 2, bias=False)
        self.conv1d = nn.Conv1d(
            in_channels=self.d_inner, out_channels=self.d_inner,
            kernel_size=d_conv, groups=self.d_inner, padding=d_conv - 1
        )
        self.x_proj = nn.Linear(self.d_inner, self.d_state * 2 + 1, bias=False)
        self.dt_proj = nn.Linear(1, self.d_inner, bias=True)
        self.out_proj = nn.Linear(self.d_inner, self.d_model, bias=False)

    def forward(self, hidden_states):
        batch, seq_len, _ = hidden_states.shape
        proj = self.in_proj(hidden_states)
        x, z = proj.chunk(2, dim=-1)
        
        x_conv = x.transpose(1, 2)
        x_conv = self.conv1d(x_conv)[:, :, :seq_len]
        x = x_conv.transpose(1, 2)
        x = torch.nn.functional.silu(x)

        x_dbl = self.x_proj(x)
        dt, B, C = torch.split(x_dbl, [1, self.d_state, self.d_state], dim=-1)
        dt = torch.nn.functional.softplus(self.dt_proj(dt))

        # Simplified Selective State Space recurrence
        y = x * dt * C.sum(dim=-1, keepdim=True)
        y = y * torch.nn.functional.silu(z)
        out = self.out_proj(y)
        
        return out
