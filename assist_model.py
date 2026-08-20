import sys
import os
import torch

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from gpt_download import load_gpt2_params_from_tf_ckpt
from GPT_Model import GPTModel
from Load_gpt2_wts_tomodel import load_weights_into_gpt

BASE_CONFIG = {
    "vocab_size": 50257,     # Vocabulary size
    "context_length": 1024,  # Context length
    "drop_rate": 0.0,        # Dropout rate
    "qkv_bias": True         # Query-key-value bias
}

model_configs = {
    "gpt2-small (124M)": {"emb_dim": 768, "n_layers": 12, "n_heads": 12},
    "gpt2-medium (355M)": {"emb_dim": 1024, "n_layers": 24, "n_heads": 16},
    "gpt2-large (774M)": {"emb_dim": 1280, "n_layers": 36, "n_heads": 20},
    "gpt2-xl (1558M)": {"emb_dim": 1600, "n_layers": 48, "n_heads": 25},
}

def setup_assist_model(device, model_choice="gpt2-medium (355M)"):
    """
    Initializes the GPT model and loads pre-trained weights.
    Returns the model ready for fine-tuning.
    """
    config = BASE_CONFIG.copy()
    config.update(model_configs[model_choice])
    
    # Extract the size string for the folder name, e.g., "355M"
    model_size = model_choice.split(" ")[-1].lstrip("(").rstrip(")")
    ckpt_dir = os.path.join(BASE_DIR, "gpt2", model_size)
    
    settings = {
        'n_vocab': 50257, 
        'n_ctx': 1024, 
        'n_embd': config["emb_dim"], 
        'n_head': config["n_heads"], 
        'n_layer': config["n_layers"]
    }
    
    params = load_gpt2_params_from_tf_ckpt(
      ckpt_dir,
      settings=settings
    )

    model = GPTModel(config)
    load_weights_into_gpt(model, params)
    
    model.to(device)
    return model, config
