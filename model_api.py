import os
import sys
import torch
import tiktoken
from flask import Flask, request, jsonify
from flask_cors import CORS

from assist_model import setup_assist_model
from assist_test import get_response

app = Flask(__name__)
CORS(app) # Allow cross-origin requests from Node.js or React

# Global variables for model and tokenizer
model = None
tokenizer = None
device = None
config = None

def init_model():
    global model, tokenizer, device, config
    
    if torch.cuda.is_available():
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        major, minor = map(int, torch.__version__.split(".")[:2])
        device = torch.device("mps") if (major, minor) >= (2, 9) else torch.device("cpu")
    else:
        device = torch.device("cpu")

    print(f"Using device: {device}")
    
    print("Setting up model...")
    model, config = setup_assist_model(device, model_choice="gpt2-medium (355M)")
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "assist_model.pth")
    if os.path.exists(model_path):
        print(f"Loading trained weights from {model_path}...")
        model.load_state_dict(torch.load(model_path, map_location=device, weights_only=True))
    else:
        print(f"Warning: Could not find '{model_path}'. Using base pretrained weights.")
        
    tokenizer = tiktoken.get_encoding("gpt2")
    print("--- Model API Ready ---")

@app.route('/chat', methods=['POST'])
def chat():
    global model, tokenizer, device, config
    
    data = request.get_json()
    if not data or 'instruction' not in data:
        return jsonify({"error": "Missing instruction in request body"}), 400
        
    instruction = data.get('instruction', '')
    input_text = data.get('input', '')
    
    try:
        response = get_response(model, instruction, input_text, tokenizer, device, config)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_model()
    # Run the microservice on port provided by HF or 7860
    port = int(os.environ.get("PORT", 7860))
    app.run(host='0.0.0.0', port=port)
