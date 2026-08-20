import os
import sys
import time
import torch
torch.set_num_threads(15)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from assist_dataset import create_dataloaders, format_input
from assist_model import setup_assist_model
from calc_loss import calc_loss_loader
from llm import train_model_simple

if __name__ == "__main__":
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        major, minor = map(int, torch.__version__.split(".")[:2])
        device = torch.device("mps") if (major, minor) >= (2, 9) else torch.device("cpu")
    else:
        device = torch.device("cpu")

    print(f"Using device: {device}")
    # torch.manual_seed(123)

    print("Loading datasets...")
    train_loader, val_loader, test_loader, tokenizer, val_data = create_dataloaders(batch_size=2, num_workers=0, allowed_max_length=256)
    
    print("Setting up model...")
    model, config = setup_assist_model(device, model_choice="gpt2-medium (355M)")
    
    model_path = os.path.join(BASE_DIR, "assist_model.pth")

    if os.path.exists(model_path):
        print(f"Found saved model! Loading weights from {model_path}...")
        model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    else:
        print("No saved model found. Training from scratch...")
        
    # Calculate initial loss
    with torch.no_grad():
        train_loss = calc_loss_loader(train_loader, model, device, num_batches=5)
        val_loss = calc_loss_loader(val_loader, model, device, num_batches=5)

    print(f"Initial Training loss: {train_loss:.4f}")
    print(f"Initial Validation loss: {val_loss:.4f}")

    start_time = time.time()
    
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.00005, weight_decay=0.1)
    num_epochs = 2

    # Start context for evaluating generation during training
    start_context = format_input(val_data[0])

    train_losses, val_losses, tokens_seen = train_model_simple(
        model, train_loader, val_loader, optimizer, device,
        num_epochs=num_epochs, eval_freq=5, eval_iter=5,
        start_context=start_context, tokenizer=tokenizer
    )

    end_time = time.time()
    execution_time_minutes = (end_time - start_time) / 60
    print(f"Training completed in {execution_time_minutes:.2f} minutes.")
    
    # Save the model weights to disk after training
    torch.save(model.state_dict(), model_path)
    print(f"Training complete. Model saved to {model_path}")