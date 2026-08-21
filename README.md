# RAIZ-GPT: 355M Parameter Foundation Model

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Deep Learning](https://img.shields.io/badge/Deep_Learning-Architecture-blue?style=for-the-badge)
![State Space Models](https://img.shields.io/badge/State_Space_Models-Mamba-green?style=for-the-badge)

RAIZ-GPT is a custom-built, 355M parameter generative language model engineered from scratch using PyTorch. This project focuses on translating deep learning research into a highly capable, low-latency foundation model, featuring robust data tokenization pipelines and experimental integrations with linear-time sequence models.

## 🚀 Key Architectural Features

* **From-Scratch Implementation:** Full control over the model architecture, avoiding high-level wrappers to deeply manipulate tensors, forward passes, and backpropagation logic.
* **Large-Scale Data Pipeline:** Engineered a highly parallel ETL (Extract, Transform, Load) data processing infrastructure to clean, evaluate, and tokenize over 100,000 unstructured instruction-response datasets.
* **Experimental SSM (Mamba) Integration:** Explored solutions to the quadratic scaling bottleneck of traditional Multi-Head Attention by implementing and testing a minimal **State Space Model (SSM)** block for linear-time sequence processing.
* **Low-Latency Inference API:** Designed a highly reliable model serving stack capable of handling real-time AI interactions.

## 🧠 State Space Model (SSM) Exploration
To optimize inference speeds and reduce memory footprint, this repository includes \MambaBlock.py\—a custom PyTorch implementation of the Mamba architecture. It utilizes 1D convolutions for local context and continuous state projections to update hidden states linearly, serving as a high-performance alternative to standard Transformer attention mechanisms. A test training script (\	rain_mamba_mini.py\) is also included to demonstrate sequence pattern convergence.

## ⚙️ Tech Stack
* **Framework:** PyTorch
* **Backend Serving:** Python, Flask, Node.js
* **Data Engineering:** Pandas, Custom Tokenizers

## 🛠️ Usage

\\ash
git clone https://github.com/romith777/RAIZ-GPT.git
cd RAIZ-GPT
pip install torch transformers pandas
python train_mamba_mini.py
\