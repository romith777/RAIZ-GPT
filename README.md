# RAIZ-GPT: 355M Parameter Foundation Model

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Transformer_%26_SSM-blue?style=for-the-badge)

RAIZ-GPT is a custom-built, 355M parameter generative language model engineered entirely from scratch using PyTorch. The project was built to deeply understand the mechanics of Large Language Models—from engineering parallelized data tokenization pipelines to implementing low-level forward/backward passes without relying on high-level abstraction libraries.

Currently, the project is actively exploring solutions to the quadratic scaling bottleneck of Multi-Head Attention by integrating experimental **State Space Models (Mamba)** for linear-time sequence processing.

## 🚀 Key Architectural Features

* **From-Scratch MHA Implementation:** Full mathematical control over the Transformer architecture, including custom multi-head attention mechanisms, layer normalizations, and positional embeddings.
* **Large-Scale ETL Pipeline:** Engineered a highly parallel data processing infrastructure to clean, evaluate, and tokenize over 100,000 unstructured instruction-response datasets prior to training.
* **The $O(N^2)$ Bottleneck & SSM Integration:** To address the memory limitations of standard attention for long contexts, this repository includes an active research branch implementing a minimal **State Space Model (SSM)** block to achieve $O(N)$ scaling.
* **Low-Latency Inference:** Designed a highly reliable model serving stack capable of handling real-time AI interactions.

## 🧠 State Space Model (Mamba) Research
Traditional Transformers suffer from $O(N^2)$ complexity. To optimize inference speeds, this repository includes `MambaBlock.py`—a custom PyTorch implementation of the Mamba architecture. It utilizes 1D convolutions for local context and continuous state projections to update hidden states linearly, serving as a high-performance alternative to standard attention.

## 🛠️ Installation & Usage

**1. Clone and Install Dependencies**
```bash
git clone https://github.com/romith777/RAIZ-GPT.git
cd RAIZ-GPT
pip install -r requirements.txt
```

**2. Standard GPT Inference (Interactive CLI)**
To test the primary 355M parameter model interactively in your terminal:
```bash
python assist_test.py
# You will be prompted to enter an instruction and context.
```

**3. Serve Model via API (Flask)**
To run the backend server (exposes a REST API on port 7860):
```bash
python app.py
```
Once the server is running, you can query the model's `/chat` endpoint using `curl` from a new terminal:
```bash
curl -X POST http://localhost:7860/chat \
     -H "Content-Type: application/json" \
     -d '{"instruction": "Explain distributed computing"}'
```

**4. Experimental SSM / Mamba Block**
To run the experimental linear-time SSM architecture on a test sequence:
```bash
# Trains a mini-Mamba block to prove sequence pattern convergence
python train_mamba_mini.py
```
