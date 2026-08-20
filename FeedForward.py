import torch
import torch.nn as nn

from GELU import GeLU

class FeedForward(nn.Module):
  def __init__(self, cfg):
    # torch.manual_seed(123)
    super().__init__()
    self.layers = nn.Sequential(
      nn.Linear(cfg["emb_dim"], 4 * cfg["emb_dim"]),
      GeLU(),
      nn.Linear(4 * cfg["emb_dim"], cfg["emb_dim"]),
    )

  def forward(self, x):
    return self.layers(x)