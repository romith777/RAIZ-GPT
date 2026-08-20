import os
import sys
import torch
import tiktoken

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from assist_model import setup_assist_model
from assist_dataset import format_input

def generate(model, idx, max_new_tokens, context_size, temperature=0.0, top_k=None, eos_id=None):
    for _ in range(max_new_tokens):
        idx_cond = idx[:, -context_size:]
        with torch.no_grad():
            logits = model(idx_cond)
        logits = logits[:, -1, :]

        # Filter logits with top_k sampling
        if top_k is not None:
            # Keep only top_k values
            top_logits, _ = torch.topk(logits, top_k)
            min_val = top_logits[:, -1]
            logits = torch.where(logits < min_val, torch.tensor(float("-inf")).to(logits.device), logits)

        # Apply temperature scaling
        if temperature > 0.0:
            logits = logits / temperature
            # numerical stability tip to get equivalent results on mps device
            # subtract rowwise max before softmax
            logits = logits - logits.max(dim=-1, keepdim=True).values
            probs = torch.softmax(logits, dim=-1)  
            idx_next = torch.multinomial(probs, num_samples=1)  
        else:
            idx_next = torch.argmax(logits, dim=-1, keepdim=True)  

        if idx_next == eos_id:  
            break

        idx = torch.cat((idx, idx_next), dim=1)  

    return idx

def token_ids_to_text(token_ids, tokenizer):
    decoded = tokenizer.decode(token_ids.squeeze(0).tolist())
    return decoded

def text_to_token_ids(text, tokenizer):
    encoded = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
    encoded_tensor = torch.tensor(encoded).unsqueeze(0)
    return encoded_tensor

def get_response(model, instruction, input_text, tokenizer, device, config):
    model.eval()
    
    entry = {
        "instruction": instruction,
        "input": input_text,
        "output": "" # empty since we want the model to generate it
    }
    
    formatted_input = format_input(entry)
    
    idx = text_to_token_ids(formatted_input, tokenizer).to(device)
    
    token_ids = generate(
        model=model,
        idx=idx,
        max_new_tokens=100, # Increased max_new_tokens for longer responses
        context_size=config["context_length"],
        eos_id=50256,
        temperature=0.7,    # Add some randomness for more natural text
        top_k=50
    )
    
    generated_text = token_ids_to_text(token_ids, tokenizer)
    
    response_text = (
        generated_text[len(formatted_input):]
        .replace("### Response:", "")
        .strip()
    )
    
    return response_text

if __name__ == "__main__":
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        major, minor = map(int, torch.__version__.split(".")[:2])
        device = torch.device("mps") if (major, minor) >= (2, 9) else torch.device("cpu")
    else:
        device = torch.device("cpu")

    print(f"Using device: {device}")
    
    # Setup model
    print("Setting up model...")
    model, config = setup_assist_model(device, model_choice="gpt2-medium (355M)")
    
    # Load weights
    model_path = os.path.join(BASE_DIR, "assist_model.pth")
    if os.path.exists(model_path):
        print(f"Loading trained weights from {model_path}...")
        model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    else:
        print(f"Warning: Could not find '{model_path}'. Using base pretrained weights. Please run assist_train.py to fine-tune the model.")
        
    tokenizer = tiktoken.get_encoding("gpt2")
    
    print("\n--- Assistant Ready ---")
    while True:
        try:
            instruction = input("\nEnter Instruction (or 'q' to quit): ")
            if instruction.lower() == 'q':
                break
                
            input_text = input("Enter Input Context (optional): ")
            
            print("\nGenerating response...")
            response = get_response(model, instruction, input_text, tokenizer, device, config)
            
            print(f"\nResponse:\n{response}")
            print("-" * 40)
            
        except KeyboardInterrupt:
            break
