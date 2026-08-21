import torch
import torch.nn as nn
from MambaBlock import SSM_MambaBlock

class MiniMambaLM(nn.Module):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        # 1. Convert token IDs to embeddings
        self.embedding = nn.Embedding(vocab_size, d_model)
        
        # 2. Our custom Mamba Block (Replaces the Transformer Block)
        self.mamba = SSM_MambaBlock(d_model=d_model)
        
        # 3. Predict the next token
        self.lm_head = nn.Linear(d_model, vocab_size)

    def forward(self, x):
        x = self.embedding(x)
        x = self.mamba(x)
        logits = self.lm_head(x)
        return logits

def train():
    print("Initializing Mini Mamba Model...")
    vocab_size = 10
    d_model = 32
    model = MiniMambaLM(vocab_size, d_model)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
    criterion = nn.CrossEntropyLoss()

    # Let's create a simple repeating pattern for it to learn
    # Pattern: 0, 1, 2, 3, 4, 0, 1, 2, 3, 4...
    sequence = [0, 1, 2, 3, 4] * 20
    
    # Input is the sequence, Target is the sequence shifted by 1
    x_data = torch.tensor([sequence[:-1]])
    y_data = torch.tensor([sequence[1:]])

    print("Starting Training to learn the pattern...")
    for epoch in range(100):
        optimizer.zero_grad()
        
        # Forward pass
        logits = model(x_data)
        
        # Calculate loss
        loss = criterion(logits.view(-1, vocab_size), y_data.view(-1))
        
        # Backpropagation
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1} | Loss: {loss.item():.4f}")

    # Save the model
    torch.save(model.state_dict(), "mamba_test_model.pth")
    print("Training Complete! Saved weights to 'mamba_test_model.pth'")

if __name__ == '__main__':
    train()