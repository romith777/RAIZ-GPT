import torch
from MambaBlock import SSM_MambaBlock

def test_mamba_block():
    print("--- Testing State Space Model (Mamba) Block ---")
    
    batch_size = 2
    seq_len = 64
    d_model = 128
    
    print(f"Creating Mamba Block with d_model={d_model}...")
    mamba_block = SSM_MambaBlock(d_model=d_model)
    
    # Dummy input
    x = torch.randn(batch_size, seq_len, d_model)
    print(f"Input Tensor Shape: {x.shape} (batch, seq_len, d_model)")
    
    # Forward pass
    out = mamba_block(x)
    print(f"Output Tensor Shape: {out.shape} (batch, seq_len, d_model)")
    
    if x.shape == out.shape:
        print("SUCCESS! The Mamba Block works and outputs the correct dimensions.")
    else:
        print("FAILED.")

if __name__ == '__main__':
    test_mamba_block()