import os
import urllib.request
import re
import torch
import tiktoken

# torch.manual_seed(123)

# print(tiktoken.__version__)

# class SimpleTokenizer:
#   def __init__(self,vocab):
#     self.str_int = vocab
#     self.int_str = {i:s for s, i in vocab.items()}

#   def encoder(self,words):
#     preprocessed = re.split(r'([,.:;?_!"()\']|--|\s)',words)
#     preprocessed = [item.strip() for item in preprocessed if item.strip()]
#     preprocessed = [item if item in self.str_int else "<|unk|>" for item in preprocessed]
#     ids = [self.str_int[s] for s in preprocessed]
#     return ids

#   def decoder(self,ids):
#     words = " ".join([self.int_str[s] for s in ids])
#     words =  re.sub(r'\s+([,.:;?_!"()\'])',r'\1', words)
#     return words

# if not os.path.exists("the-verdict.txt"):
#   url=("https://raw.githubusercontent.com/rasbt/LLMs-from-scratch/refs/heads/main/ch02/01_main-chapter-code/the-verdict.txt")
#   file_path="the-verdict.txt"
#   urllib.request.urlretrieve(url,file_path)

# with open("the-verdict.txt", "r", encoding="utf-8") as file:
#   raw_text=file.read()

# preprocessed=re.split(r'([,.:;?_!"()\']|--|\s)',raw_text)
# preprocessed = [item for item in preprocessed if item.strip()]
# all_tokens=sorted(list(set(preprocessed)))
# all_tokens.extend(["<|endoftext|>","<|unk|>"])


# vocab={token: integer for integer, token in enumerate(all_tokens)}
# # print(list(vocab.items())[-2:])
# # for i,item in enumerate(list(vocab.items())[-5:]):
# #   print("asd")
# #   print(item)

# text="this is a line, which is called as a sentence."
# tokenizer = SimpleTokenizer(vocab)

# ids = tokenizer.encoder(text)
# print(ids)

# line=tokenizer.decoder(ids)
# print(line)

# # ---------BYTE PAIR ENCODING----------

# tokenizer=tiktoken.get_encoding("gpt2")


# # --------DATA SAMPLING WITH SLIDING WINDOW-------

# with open("the-verdict.txt","r",encoding="utf-8") as file:
#   raw_text=file.read()

# tokenizer=tiktoken.get_encoding("gpt2")
# enc_text=tokenizer.encode(raw_text)
# print(len(enc_text))

# enc_sample = enc_text[50:]
# context_size=4 #sample window

# x=enc_sample[:context_size]
# y=enc_sample[1:context_size+1]

# print(f"x:{x}")
# print(f"y:     {y}")

# from torch.utils.data import Dataset, DataLoader

# class GPTDatasetV1(Dataset):
#   def __init__(self, txt, tokenizer, max_length, stride):
#     self.input_ids=[]
#     self.target_ids=[]

#     #tokenize the text
#     token_ids=tokenizer.encode(txt, allowed_special={"<|endoftext|>"})

#     #use a sliding window to chunk the book into overlapping sequences of max_length
#     for i in range(0, len(token_ids) - max_length, stride):
#       input_chunk = token_ids[i:i+max_length]
#       target_chunk = token_ids[i+1:i+max_length+1]
#       self.input_ids.append(torch.tensor(input_chunk))
#       self.target_ids.append(torch.tensor(target_chunk))
#   def __len__(self):
#     return len(self.input_ids)
#   def __getitem__(self, index):
#     return self.input_ids[index], self.target_ids[index]

# def create_dataloader_v1(txt, batch_size=4, max_length=256, stride=128, shuffle=True, drop_last=True, num_workers=0):

#   #tokenizer
#   tokenizer=tiktoken.get_encoding("gpt2")

#   #dataset
#   dataset=GPTDatasetV1(txt, tokenizer, max_length, stride)

#   #dataloader
#   dataloader= DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, drop_last=drop_last, num_workers=num_workers)

#   return dataloader

# with open("the-verdict.txt", "r", encoding="utf-8") as file:
#   raw_text=file.read()

# # dataloader = create_dataloader_v1(raw_text, batch_size=8, max_length=4, stride=4, shuffle=False)

# # data_iter=iter(dataloader)
# # inputs, targets=next(data_iter)
# # print("Inputs:\n",inputs)
# # print("Targets:\n",targets)

# # --------CREATING TOKEN EMBEDDINGS--------

# # input_ids = torch.tensor([2, 3, 5, 1])

# # vocab_size=6
# # output_dim=3

# # torch.manual_seed(123)
# # embedding_layer=torch.nn.Embedding(vocab_size, output_dim)

# # print(embedding_layer.weight)

# # --------ENCODING WORD POSITIONS--------

# vocab_size=50257
# output_dim=256

# token_embedding_layer=torch.nn.Embedding(vocab_size, output_dim)

# max_length=4

# dataloader = create_dataloader_v1(raw_text, batch_size=8, max_length=4, stride=4, shuffle=False)

# data_iter=iter(dataloader)
# inputs, targets=next(data_iter)

# token_embeddings = token_embedding_layer(inputs)
# # print(token_embeddings[0, 0])

# context_length = max_length
# pos_embedding_layer=torch.nn.Embedding(context_length, output_dim)

# # print(pos_embedding_layer.weight)
# pos_embeddings = pos_embedding_layer(torch.arange(max_length))
# # print(pos_embeddings)
# # print(token_embeddings.shape)
# # print(pos_embeddings.shape)

# input_embeddings=token_embeddings+pos_embeddings
# print(input_embeddings.shape)

# --------CHAPTER 3--------
# --------CODING ATTENTION MECHANISMS--------

# import torch

# inputs=torch.tensor(
#   [[0.43, 0.15, 0.89],
#    [0.55, 0.87, 0.66],
#    [0.57, 0.85, 0.64],
#    [0.22, 0.58, 0.33],
#    [0.77, 0.25, 0.10],
#    [0.05, 0.80, 0.55]]
# )

# attn_scores = torch.empty(inputs.shape[0],inputs.shape[0])
# # for i,x_i in enumerate(inputs):
# #   for j,x_j in enumerate(inputs):
# #     attn_scores[i,j]=torch.dot(x_i, x_j)
# # print(attn_scores)

# attn_scores = inputs @ inputs.T
# # print(attn_scores)

# attn_weights = torch.softmax(attn_scores, dim=1)
# # print(attn_weights)

# all_context_vec = attn_weights @ inputs
# print(all_context_vec)
# for i,x_i in enumerate(inputs):
#   context_vec_2+=attn_weights_2_tmp[i]*x_i
# print(context_vec_2)

# --------IMPLEMENTING SELF-ATTENTION WITH TRAINABLE WEIGHTS--------

# x_2 = inputs[1]
# d_in = inputs.shape[1]
# d_out = 2

# torch.manual_seed(789)

# W_query = torch.nn.Parameter(torch.rand(d_in, d_out))
# W_key = torch.nn.Parameter(torch.rand(d_in, d_out))
# W_value = torch.nn.Parameter(torch.rand(d_in, d_out))

# print(W_query)
# print(W_key)
# print(W_value)

# query_2 = x_2 @ W_query
# key = inputs @ W_key
# value = inputs @ W_value

# # attn_score_22 = torch.dot(query_2, key[1])
# # print(attn_score_22)

# attn_score_2 = query_2 @ key.T
# # print(attn_score_2)

# d_k = key.shape[1]
# # print(key)

# attn_weights_2 = torch.softmax(attn_score_2 / d_k**0.5, dim=-1)
# # print(attn_weights_2)

# context_vec_2 = attn_weights_2 @ value
# print(context_vec_2)


# --------IMPLEMENTING A COMPACT SELFATTENTION CLASS--------

import torch.nn as nn

# class SelfAttention_v1(nn.Module):
#   def __init__(self, d_in, d_out, qkv_bias=False):
#     super().__init__()
#     # self.W_query = torch.nn.Parameter(torch.rand(d_in, d_out))
#     #self.W_key = torch.nn.Parameter(torch.rand(d_in, d_out))
#     #self.W_value = torch.nn.Parameter(torch.rand(d_in, d_out))
#     self.W_query = torch.nn.Linear(d_in, d_out, bias=qkv_bias)
#     self.W_key = torch.nn.Linear(d_in, d_out, bias=qkv_bias)
#     self.W_value = torch.nn.Linear(d_in, d_out, bias=qkv_bias)

#   def forward(self, inputs):
#     # queries = inputs @ W_query
#     # keys = inputs @ W_key
#     # values = inputs @ W_value

#     queries = self.W_query(inputs)
#     keys = self.W_key(inputs)
#     values = self.W_value(inputs)

#     attn_score = queries @ keys.T
#     attn_weights = torch.softmax(attn_score / keys.shape[1]**0.5, dim=-1)
#     context_vec = attn_weights @ values

#     return context_vec

# sa_v1 = SelfAttention_v1(d_in, d_out)
# # print(sa_v1(inputs))

# queries = sa_v1.W_query(inputs)
# keys = sa_v1.W_key(inputs)
# values = sa_v1.W_value(inputs)

# attn_score = queries @ keys.T
# # attn_weights = torch.softmax(attn_score / keys.shape[1]**0.5, dim=-1)

# context_len = attn_score.shape[0]
# # mask_simple = torch.tril(torch.ones(context_len, context_len))

# # masked_simple = attn_weights * mask_simple

# # row_sums = masked_simple.sum(dim=-1, keepdim=True)
# # masked_simple_norm = masked_simple/row_sums

# mask = torch.triu (torch.ones(context_len, context_len), diagonal=1)
# masked = attn_score.masked_fill(mask.bool(), -torch.inf)

# attn_weights = torch.softmax(masked / keys.shape[-1]**0.5, dim=-1)

# print(attn_weights)


# implementing compact self attention 

# class CasualAttention_v1(nn.Module):
#   def __init__(self, d_in, d_out, context_len, dropout, qkv_bias=False):
#     super().__init__()
#     # self.W_query = torch.nn.Parameter(torch.rand(d_in, d_out))
#     #self.W_key = torch.nn.Parameter(torch.rand(d_in, d_out))
#     #self.W_value = torch.nn.Parameter(torch.rand(d_in, d_out))
#     self.W_query = torch.nn.Linear(d_in, d_out, bias=qkv_bias)
#     self.W_key = torch.nn.Linear(d_in, d_out, bias=qkv_bias)
#     self.W_value = torch.nn.Linear(d_in, d_out, bias=qkv_bias)
#     self.dropout = torch.nn.Dropout(dropout)
#     self.register_buffer("mask", torch.triu(torch.ones(context_len, context_len), diagonal=1))

#   def forward(self, inputs):
#     # queries = inputs @ W_query
#     # keys = inputs @ W_key
#     # values = inputs @ W_value
#     b, num_tokens, d_in = inputs.shape
#     queries = self.W_query(inputs)
#     keys = self.W_key(inputs)
#     values = self.W_value(inputs)

#     attn_score = queries @ keys.transpose(1,2)
#     attn_score.masked_fill_(self.mask.bool()[:num_tokens, :num_tokens], -torch.inf)
#     attn_weights = torch.softmax(attn_score/keys.shape[-1]**0.5, dim=-1)
#     attn_weights = self.dropout(attn_weights)

#     context_vec = attn_weights @ values

#     return context_vec

# batch = torch.stack((inputs, inputs), dim=0)

# context_len = batch.shape[1]
# dropout = 0.0
# d_in = 3
# d_out=2

# ca = CasualAttention_v1(d_in, d_out, context_len, dropout)
# # ca(batch)
# # print(ca(batch))


# class MultiHeadAttentionWrapper(nn.Module):
#     def __init__(self, d_in, d_out, context_length, dropout, num_heads, qkv_bias=False):
#         super().__init__()
#         assert d_out % num_heads == 0, "d_out must be divisible by num_heads"

#         self.d_out = d_out
#         self.num_heads = num_heads
#         self.head_dim = d_out // num_heads  # Reduce the projection dim to match desired output dim

#         self.W_query = nn.Linear(d_in, d_out, bias=qkv_bias)
#         self.W_key = nn.Linear(d_in, d_out, bias=qkv_bias)
#         self.W_value = nn.Linear(d_in, d_out, bias=qkv_bias)
#         self.out_proj = nn.Linear(d_out, d_out)  # Linear layer to combine head outputs
#         self.dropout = nn.Dropout(dropout)
#         self.register_buffer("mask", torch.triu(torch.ones(context_length, context_length), diagonal=1))

#     def forward(self, x):
#         b, num_tokens, d_in = x.shape

#         keys = self.W_key(x)  # Shape: (b, num_tokens, d_out)
#         queries = self.W_query(x)
#         values = self.W_value(x)

#         # We implicitly split the matrix by adding a `num_heads` dimension
#         # Unroll last dim: (b, num_tokens, d_out) -> (b, num_tokens, num_heads, head_dim)
#         keys = keys.view(b, num_tokens, self.num_heads, self.head_dim)
#         values = values.view(b, num_tokens, self.num_heads, self.head_dim)
#         queries = queries.view(b, num_tokens, self.num_heads, self.head_dim)

#         # Transpose: (b, num_tokens, num_heads, head_dim) -> (b, num_heads, num_tokens, head_dim)
#         keys = keys.transpose(1, 2)
#         queries = queries.transpose(1, 2)
#         values = values.transpose(1, 2)

#         # Compute scaled dot-product attention (aka self-attention) with a causal mask
#         attn_scores = queries @ keys.transpose(2, 3)  # Dot product for each head

#         # Original mask truncated to the number of tokens and converted to boolean
#         mask_bool = self.mask.bool()[:num_tokens, :num_tokens]

#         # Use the mask to fill attention scores
#         attn_scores.masked_fill_(mask_bool, -torch.inf)

#         attn_weights = torch.softmax(attn_scores / keys.shape[-1]**0.5, dim=-1)
#         attn_weights = self.dropout(attn_weights)

#         # Shape: (b, num_tokens, num_heads, head_dim)
#         context_vec = (attn_weights @ values).transpose(1, 2)

#         # Combine heads, where self.d_out = self.num_heads * self.head_dim
#         context_vec = context_vec.contiguous().view(b, num_tokens, self.d_out)
#         context_vec = self.out_proj(context_vec)  # optional projection

#         return context_vec


# torch.manual_seed(123)
# mha = MultiHeadAttentionWrapper(d_in, d_out, context_len, dropout=0.0, num_heads=2)
# print(mha(batch))

# -------- CHAPTER 4 --------

# --------LLM ARCHITECTURE--------

# import torch
# import torch.nn as nn

GPT_CONFIG_124M = {
    "vocab_size": 50257,    # Vocabulary size
    "context_length": 1024, # Context length
    "emb_dim": 768,         # Embedding dimension
    "n_heads": 12,          # Number of attention heads
    "n_layers": 12,         # Number of layers
    "drop_rate": 0.1,       # Dropout rate
    "qkv_bias": False       # Query-Key-Value bias
}

# class DummyGPTModel(nn.Module):
#   def __init__(self, cfg):
#     super().__init__()
#     self.tok_emb = nn.Embedding(cfg["vocab_size"], cfg["emb_dim"])
#     self.pos_emb = nn.Embedding(cfg["context_length"], cfg["emb_dim"])
#     self.drop_emb = nn.Dropout(cfg["drop_rate"])
    
#     # Use a placeholder for TransformerBlock
#     self.trf_blocks = nn.Sequential(
#       *[DummyTransformerBlock(cfg) for _ in range(cfg["n_layers"])])
    
#     # Use a placeholder for LayerNorm
#     self.final_norm = DummyLayerNorm(cfg["emb_dim"])
#     self.out_head = nn.Linear(
#       cfg["emb_dim"], cfg["vocab_size"], bias=False
#     )

#   def forward(self, in_idx):
#     batch_size, seq_len = in_idx.shape
#     tok_embeds = self.tok_emb(in_idx)
#     pos_embeds = self.pos_emb(torch.arange(seq_len, device=in_idx.device))
#     x = tok_embeds + pos_embeds
#     x = self.drop_emb(x)
#     x = self.trf_blocks(x)
#     x = self.final_norm(x)
#     logits = self.out_head(x)
#     return logits


# class DummyTransformerBlock(nn.Module):
#   def __init__(self, cfg):
#     super().__init__()
#     # A simple placeholder

#   def forward(self, x):
#     # This block does nothing and just returns its input.
#     return x


# class DummyLayerNorm(nn.Module):
#   def __init__(self, normalized_shape, eps=1e-5):
#     super().__init__()
#     # The parameters here are just to mimic the LayerNorm interface.

#   def forward(self, x):
#     # This layer does nothing and just returns its input.
#     return x

# import tiktoken

# tokenizer = tiktoken.get_encoding("gpt2")

# batch = []

# txt1 = "Every effort moves you"
# txt2 = "Every day holds a"

# batch.append(torch.tensor(tokenizer.encode(txt1)))
# batch.append(torch.tensor(tokenizer.encode(txt2)))
# batch = torch.stack(batch, dim=0)
# print(batch)

# torch.manual_seed(123)
# model = DummyGPTModel(GPT_CONFIG_124M)

# logits = model(batch)
# print("Output shape:", logits.shape)
# print(logits)

# --------NORMALIZING ACTIVATIONS WITH LAYER NORMALIZATION--------
# torch.manual_seed(123)

# batch_example = torch.randn(2,5)
# # print(batch_example)

# layer = nn.Sequential(nn.Linear(5,6), nn.ReLU())
# out = layer(batch_example)
# # print(out)

# mean = torch.mean(out, dim=-1, keepdim=True)
# var = torch.var(out, dim=-1, keepdim=True)

# out_norm = (out - mean) / torch.sqrt(var)

# print(out_norm.mean(dim=-1, keepdim=True))

# print(out_norm)

# class LayerNorm(nn.Module):
#   def __init__(self, emb_dim):
#     super().__init__()
#     self.eps = 1e-5
#     self.scale = nn.Parameter(torch.ones(emb_dim))
#     self.shift = nn.Parameter(torch.zeros(emb_dim))

#   def forward(self, x):
#     mean = x.mean(dim=-1, keepdim=True)
#     var = x.var(dim=-1, keepdim=True, unbiased=False)
#     norm_x = (x - mean) / torch.sqrt(var + self.eps)
#     return self.scale * norm_x + self.shift

# # --------GELU ACTIVATION--------

# class GELU(nn.Module):
#   def __init__(self):
#     super().__init__()

#   def forward(self, x):
#     return 0.5 * x * (1 + torch.tanh(
#       torch.sqrt(torch.tensor(2.0 / torch.pi)) * 
#       (x + 0.044715 * torch.pow(x, 3))
#     ))

# # --------FEED FORWARD NETWORK--------

# class FeedForward(nn.Module):
#   def __init__(self, cfg):
#     super().__init__()
#     self.layers = nn.Sequential(
#       nn.Linear(cfg["emb_dim"], 4 * cfg["emb_dim"]),
#       GELU(),
#       nn.Linear(4 * cfg["emb_dim"], cfg["emb_dim"]),
#     )

#   def forward(self, x):
#     return self.layers(x)

# ffn = FeedForward(GPT_CONFIG_124M)

# # input shape: [batch_size, num_token, emb_size]
# x = torch.rand(2, 3, 768) 
# out = ffn(x)
# print(out.shape)



# # --------SHORTCUT CONNECTIONS--------

# class ExampleDeepNeuralNetwork(nn.Module):
#   def __init__(self, layer_sizes, use_shortcut):
#     super().__init__()
#     self.use_shortcut = use_shortcut
#     self.layers = nn.ModuleList([
#       nn.Sequential(nn.Linear(layer_sizes[0], layer_sizes[1]), GELU()),
#       nn.Sequential(nn.Linear(layer_sizes[1], layer_sizes[2]), GELU()),
#       nn.Sequential(nn.Linear(layer_sizes[2], layer_sizes[3]), GELU()),
#       nn.Sequential(nn.Linear(layer_sizes[3], layer_sizes[4]), GELU()),
#       nn.Sequential(nn.Linear(layer_sizes[4], layer_sizes[5]), GELU())
#     ])

# def forward(self, x):
#   for layer in self.layers:
#     # Compute the output of the current layer
#     layer_output = layer(x)
#     # Check if shortcut can be applied
#     if self.use_shortcut and x.shape == layer_output.shape:
#       x = x + layer_output
#     else:
#       x = layer_output
#   return x


# def print_gradients(model, x):
#   # Forward pass
#   output = model(x)
#   target = torch.tensor([[0.]])

#   # Calculate loss based on how close the target
#   # and output are
#   loss = nn.MSELoss()
#   loss = loss(output, target)
  
#   # Backward pass to calculate the gradients
#   loss.backward()

#   for name, param in model.named_parameters():
#     if 'weight' in name:
#       # Print the mean absolute gradient of the weights
#       print(f"{name} has gradient mean of {param.grad.abs().mean().item()}")

# from MHA import MultiHeadAttentionWrapper

# class TransformerBlock(nn.Module):
#   def __init__(self, cfg):
#     super().__init__()
#     self.att = MultiHeadAttentionWrapper(
#         d_in=cfg["emb_dim"],
#         d_out=cfg["emb_dim"],
#         context_length=cfg["context_length"],
#         num_heads=cfg["n_heads"], 
#         dropout=cfg["drop_rate"],
#         qkv_bias=cfg["qkv_bias"])
#     self.ff = FeedForward(cfg)
#     self.norm1 = LayerNorm(cfg["emb_dim"])
#     self.norm2 = LayerNorm(cfg["emb_dim"])
#     self.drop_shortcut = nn.Dropout(cfg["drop_rate"])

#   def forward(self, x):
#     # Shortcut connection for attention block
#     shortcut = x
#     x = self.norm1(x)
#     x = self.att(x)  # Shape [batch_size, num_tokens, emb_size]
#     x = self.drop_shortcut(x)
#     x = x + shortcut  # Add the original input back

#     # Shortcut connection for feed forward block
#     shortcut = x
#     x = self.norm2(x)
#     x = self.ff(x)
#     x = self.drop_shortcut(x)
#     x = x + shortcut  # Add the original input back

#     return x


tokenizer = tiktoken.get_encoding("gpt2")

# batch = []

# txt1 = "Every effort moves you"
# txt2 = "Every day holds a"

# batch.append(torch.tensor(tokenizer.encode(txt1)))
# batch.append(torch.tensor(tokenizer.encode(txt2)))

# batch = torch.stack(batch, dim=0)
# print(batch)

from GPT_Model import GPTModel
from GPT_CONFIG_124M import GPT_CONFIG_124M

# torch.manual_seed(123)
model = GPTModel(GPT_CONFIG_124M)

# out = model(batch)

# print(out.shape)



# start = "Hello, I am"

# encoded = tokenizer.encode(start)
# encoded_tensor = torch.tensor(encoded).unsqueeze(0)

# output = generate_sample_text(model=model, idx=encoded_tensor, max_new_tokens=6, context_size=GPT_CONFIG_124M["context_length"])

# print(tokenizer.decode(((output).squeeze(0)).tolist()))

# torch.manual_seed(123)
# model = GPTModel(GPT_CONFIG_124M)
# model.eval()



# tokenizer = tiktoken.get_encoding("gpt2")
# start_context="Every effort moves you"


# token_ids=text_to_token_ids(start_context, tokenizer=tokenizer)

# # print(text_to_token_ids(start_context, tokenizer=tokenizer))

# out = generate_sample_text(model, token_ids, max_new_tokens=11, context_size=1024)
# # print(out)



# out = token_ids_to_text(out, tokenizer)

# print(out)

# torch.manual_seed(123)


# inputs = torch.tensor([[16833, 3626, 6100],[40, 1170, 588]])
# targets = torch.tensor([[3626, 6100, 345], [1107, 588, 11311]])

# # print(inputs.shape)
# with torch.no_grad():
#   logits = model(inputs)

# probas = torch.softmax(logits, dim=-1)

# inputs_out = torch.argmax(probas, dim=-1, keepdim=True)
# inputs_target = token_ids_to_text(inputs_out[0].flatten(), tokenizer)

# # print(token_ids_to_text(inputs[0], tokenizer))
# # print(inputs_target)

# text_ids = 0
# target_probas_1 = probas[text_ids, [0,1,2], targets[text_ids]]
# # print(target_probas_1)

# # print(probas.shape)
# # print(probas)

# logits_flat = logits.flatten(0,1)
# targets_flat = targets.flatten()
# # print(logits_flat.shape)

# #Logits---->Probabilities----->target probabilites----->log probabilities---->avg log prob----->negative avg log prob = crossentropy value

# crossentroyLos = torch.nn.functional.cross_entropy(logits_flat, targets_flat)
# print(crossentroyLos)


# print("Train_loader:")
# for x, y in train_loader:
#   pass
# print(x.shape, y.shape)

# train_tokens = 0
# for input_batch, target_batch in train_loader:
#   train_tokens+=input_batch.numel()

# val_tokens = 0
# for input_batch, target_batch in val_loader:
#   val_tokens+=input_batch.numel()

# print(f"Train Tokens: {train_tokens}, Val Tokens: {val_tokens}, Total Tokens: {train_tokens+val_tokens}")

# def calc_loss_batch(input_batch, target_batch, model, device):
#   input_batch, target_batch = input_batch.to(device), target_batch.to(device)
#   logits = model(input_batch)
#   loss = torch.nn.functional.cross_entropy(logits.flatten(0, 1), target_batch.flatten())
#   return loss

# def calc_loss_loader(data_loader, model, device, num_batches=None):
#   total_loss=0
#   if len(data_loader)==0:
#     return float("nan")
#   elif num_batches is None:
#     num_batches=len(data_loader)
#   else:
#     # reduce the number of batches to match the total number of batches in the data loader
#     # if num_batches exceeds the number of batches in the data loader
#     num_batches = min(num_batches, len(data_loader))

#   for i, (input_batch, target_batch) in enumerate(data_loader):
#     if i < num_batches:
#       loss = calc_loss_batch(input_batch, target_batch, model, device)
#       total_loss+=loss.item()
#     else:
#       break
#   return total_loss/num_batches


# torch.manual_seed(123)

# with torch.no_grad():
#   train_loss = calc_loss_loader(train_loader, model, device)
#   val_loss = calc_loss_loader(val_loader, model, device)

# print(f"{train_loss}, {val_loss}")

from calc_loss import calc_loss_loader, calc_loss_batch

with open("the-verdict.txt", "r", encoding="utf-8") as file:
  text_data = file.read()

# print(text_data[:10])

from dataLoader import create_dataloader_v1

GPT_CONFIG_124M = {
  "vocab_size": 50257,    # Vocabulary size
  "context_length": 256, # Context length
  "emb_dim": 768,         # Embedding dimension
  "n_heads": 12,          # Number of attention heads
  "n_layers": 12,         # Number of layers
  "drop_rate": 0.1,       # Dropout rate
  "qkv_bias": False       # Query-Key-Value bias
}

def generate(model, idx, max_new_tokens, context_size, temperature=0.0, top_k=None, eos_id=None):
  for _ in range(max_new_tokens):
    idx_cond = idx[:, -context_size:]
    with torch.no_grad():
      logits = model(idx_cond)
    logits = logits[:,-1,:]
    # probas = torch.softmax(logits, dim=-1)
    if top_k is not None:
      top_logits, top_pos = torch.topk(logits, top_k)
      logits = torch.where(condition=logits<top_logits[:, -1:], input=torch.tensor(float("-inf")), other=logits)
    if temperature > 0.0:
      logits = logits / temperature
      probas = torch.softmax(logits, dim=-1)
      idx_next = torch.multinomial(probas, num_samples=1)
    else:
      idx_next = torch.argmax(logits, dim=-1, keepdim=True)
    if idx_next == eos_id:
      break
    idx = torch.cat((idx, idx_next), dim=-1)
  return idx

def token_ids_to_text(token_ids, tokenizer):
  decoded = tokenizer.decode(token_ids.squeeze(0).tolist())
  return decoded

def text_to_token_ids(text, tokenizer):
  encoded = tokenizer.encode(text, allowed_special={"<|endoftext|>"})
  encoded_tensor = torch.tensor(encoded).unsqueeze(0)
  return encoded_tensor

def train_model_simple(model, train_loader, val_loader, optimizer, device, num_epochs,
                       eval_freq, eval_iter, start_context, tokenizer):
    # Initialize lists to track losses and tokens seen
    train_losses, val_losses, track_tokens_seen = [], [], []
    tokens_seen, global_step = 0, -1

    # Main training loop
    for epoch in range(num_epochs):
        model.train()  # Set model to training mode
        
        for input_batch, target_batch in train_loader:
            optimizer.zero_grad() # Reset loss gradients from previous batch iteration
            loss = calc_loss_batch(input_batch, target_batch, model, device)
            loss.backward() # Calculate loss gradients
            optimizer.step() # Update model weights using loss gradients
            tokens_seen += input_batch.numel()
            global_step += 1

            # Optional evaluation step
            if global_step % eval_freq == 0:
                train_loss, val_loss = evaluate_model(
                    model, train_loader, val_loader, device, eval_iter)
                train_losses.append(train_loss)
                val_losses.append(val_loss)
                track_tokens_seen.append(tokens_seen)
                print(f"Ep {epoch+1} (Step {global_step:06d}): "
                      f"Train loss {train_loss:.3f}, Val loss {val_loss:.3f}")

        # Print a sample text after each epoch
        generate_and_print_sample(
            model, tokenizer, device, start_context
        )

    return train_losses, val_losses, track_tokens_seen


def evaluate_model(model, train_loader, val_loader, device, eval_iter):
    model.eval()
    with torch.no_grad():
        train_loss = calc_loss_loader(train_loader, model, device, num_batches=eval_iter)
        val_loss = calc_loss_loader(val_loader, model, device, num_batches=eval_iter)
    model.train()
    return train_loss, val_loss


def generate_and_print_sample(model, tokenizer, device, start_context):
    model.eval()
    context_size = model.pos_emb.weight.shape[0]
    encoded = text_to_token_ids(start_context, tokenizer).to(device)
    with torch.no_grad():
        token_ids = generate(
            model=model, idx=encoded,
            max_new_tokens=50, context_size=context_size
        )
    decoded_text = token_ids_to_text(token_ids, tokenizer)
    print(decoded_text.replace("\n", " "))  # Compact print format
    model.train()

# train_ratio = 0.90
# split_idx = int(train_ratio * len(text_data))
# train_data = text_data[:split_idx]
# val_data = text_data[split_idx:]

# train_loader = create_dataloader_v1(train_data, batch_size=2, max_length=GPT_CONFIG_124M["context_length"],stride=GPT_CONFIG_124M["context_length"], drop_last=True, shuffle=True, num_workers=0)
# val_loader = create_dataloader_v1(val_data, batch_size=2, max_length=GPT_CONFIG_124M["context_length"],stride=GPT_CONFIG_124M["context_length"], drop_last=False, shuffle=False, num_workers=0)



# # torch.manual_seed(123)
# model = GPTModel(GPT_CONFIG_124M)
# model.to(device)
# optimizer = torch.optim.AdamW(model.parameters(), lr=0.0004, weight_decay=0.1)

# num_epochs = 30
# train_losses, val_losses, token_seen = train_model_simple(model, train_loader, val_loader, optimizer, device, num_epochs=num_epochs, eval_freq=5, eval_iter=5, start_context="Every effort moves you", tokenizer=tokenizer)

# print(token_ids_to_text(generate(model=model, idx=text_to_token_ids("Every effort moves you", tokenizer), max_new_tokens=15, context_size=GPT_CONFIG_124M["context_length"]), tokenizer))


# from gpt_download import download_and_load_gpt2, load_gpt2_params_from_tf_ckpt

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# params = load_gpt2_params_from_tf_ckpt(ckpt_path="./gpt2/124M", settings={'n_vocab': 50257, 'n_ctx': 1024, 'n_embd': 768, 'n_head': 12, 'n_layer': 12})
# print(settings)

# Define model configurations in a dictionary for compactness
# model_configs = {
#   "gpt2-small (124M)": {"emb_dim": 768, "n_layers": 12, "n_heads": 12},
#   "gpt2-medium (355M)": {"emb_dim": 1024, "n_layers": 24, "n_heads": 16},
#   "gpt2-large (774M)": {"emb_dim": 1280, "n_layers": 36, "n_heads": 20},
#   "gpt2-xl (1558M)": {"emb_dim": 1600, "n_layers": 48, "n_heads": 25},
# }

# # Copy the base configuration and update with specific model settings
# model_name = "gpt2-small (124M)"  # Example model name
# NEW_CONFIG = GPT_CONFIG_124M.copy()
# NEW_CONFIG.update(model_configs[model_name])
# NEW_CONFIG.update({"context_length": 1024, "qkv_bias": True})
# # print(NEW_CONFIG)
# gpt = GPTModel(NEW_CONFIG)
# gpt.eval()

# def assign(left, right):
#   if left.shape != right.shape:
#     raise ValueError(f"Shape mismatch. Left: {left.shape}, Right: {right.shape}")
#   return torch.nn.Parameter(torch.tensor(right))

# import numpy as np

# def load_weights_into_gpt(gpt, params):
#     gpt.pos_emb.weight = assign(gpt.pos_emb.weight, params['wpe'])
#     gpt.tok_emb.weight = assign(gpt.tok_emb.weight, params['wte'])
    
#     for b in range(len(params["blocks"])):
#         q_w, k_w, v_w = np.split(
#             (params["blocks"][b]["attn"]["c_attn"])["w"], 3, axis=-1)
#         gpt.trf_blocks[b].att.W_query.weight = assign(
#             gpt.trf_blocks[b].att.W_query.weight, q_w.T)
#         gpt.trf_blocks[b].att.W_key.weight = assign(
#             gpt.trf_blocks[b].att.W_key.weight, k_w.T)
#         gpt.trf_blocks[b].att.W_value.weight = assign(
#             gpt.trf_blocks[b].att.W_value.weight, v_w.T)

#         q_b, k_b, v_b = np.split(
#             (params["blocks"][b]["attn"]["c_attn"])["b"], 3, axis=-1)
#         gpt.trf_blocks[b].att.W_query.bias = assign(
#             gpt.trf_blocks[b].att.W_query.bias, q_b)
#         gpt.trf_blocks[b].att.W_key.bias = assign(
#             gpt.trf_blocks[b].att.W_key.bias, k_b)
#         gpt.trf_blocks[b].att.W_value.bias = assign(
#             gpt.trf_blocks[b].att.W_value.bias, v_b)

#         gpt.trf_blocks[b].att.out_proj.weight = assign(
#             gpt.trf_blocks[b].att.out_proj.weight, 
#             params["blocks"][b]["attn"]["c_proj"]["w"].T)
#         gpt.trf_blocks[b].att.out_proj.bias = assign(
#             gpt.trf_blocks[b].att.out_proj.bias, 
#             params["blocks"][b]["attn"]["c_proj"]["b"])

#         gpt.trf_blocks[b].ff.layers[0].weight = assign(
#             gpt.trf_blocks[b].ff.layers[0].weight, 
#             params["blocks"][b]["mlp"]["c_fc"]["w"].T)
#         gpt.trf_blocks[b].ff.layers[0].bias = assign(
#             gpt.trf_blocks[b].ff.layers[0].bias, 
#             params["blocks"][b]["mlp"]["c_fc"]["b"])
#         gpt.trf_blocks[b].ff.layers[2].weight = assign(
#             gpt.trf_blocks[b].ff.layers[2].weight, 
#             params["blocks"][b]["mlp"]["c_proj"]["w"].T)
#         gpt.trf_blocks[b].ff.layers[2].bias = assign(
#             gpt.trf_blocks[b].ff.layers[2].bias, 
#             params["blocks"][b]["mlp"]["c_proj"]["b"])

#         gpt.trf_blocks[b].norm1.scale = assign(
#             gpt.trf_blocks[b].norm1.scale, 
#             params["blocks"][b]["ln_1"]["g"])
#         gpt.trf_blocks[b].norm1.shift = assign(
#             gpt.trf_blocks[b].norm1.shift, 
#             params["blocks"][b]["ln_1"]["b"])
#         gpt.trf_blocks[b].norm2.scale = assign(
#             gpt.trf_blocks[b].norm2.scale, 
#             params["blocks"][b]["ln_2"]["g"])
#         gpt.trf_blocks[b].norm2.shift = assign(
#             gpt.trf_blocks[b].norm2.shift, 
#             params["blocks"][b]["ln_2"]["b"])

#     gpt.final_norm.scale = assign(gpt.final_norm.scale, params["g"])
#     gpt.final_norm.shift = assign(gpt.final_norm.shift, params["b"])
#     gpt.out_head.weight = assign(gpt.out_head.weight, params["wte"])
    
    
# load_weights_into_gpt(gpt, params)
# gpt.to(device)

# torch.manual_seed(1232134)

# token_ids = generate(
#     model=gpt,
#     idx=text_to_token_ids("how can you even", tokenizer).to(device),
#     max_new_tokens=25,
#     context_size=NEW_CONFIG["context_length"],
#     top_k=50,
#     temperature=1.5
# )

# print("Output text:\n", token_ids_to_text(token_ids, tokenizer))

# import pandas as pd

# df=pd.read_csv('./sms_spam_collection/SMSSpamCollection.tsv', sep='\t', header=None, names=["Label", "Text"])
# # print(df)

# def create_balanced_dataset(df):
    
#     # Count the instances of "spam"
#     num_spam = df[df["Label"] == "spam"].shape[0]
    
#     # Randomly sample "ham" instances to match the number of "spam" instances
#     ham_subset = df[df["Label"] == "ham"].sample(num_spam, random_state=123)
    
#     # Combine ham "subset" with "spam"
#     balanced_df = pd.concat([ham_subset, df[df["Label"] == "spam"]])

#     return balanced_df


# balanced_df = create_balanced_dataset(df)
# # print(balanced_df["Label"].value_counts())

# balanced_df["Label"] = balanced_df["Label"].map({"ham": 0, "spam": 1})
# # print(balanced_df)

# def random_split(df, train_frac, validation_frac):
#     # Shuffle the entire DataFrame
#     df = df.sample(frac=1, random_state=123).reset_index(drop=True)

#     # Calculate split indices
#     train_end = int(len(df) * train_frac)
#     validation_end = train_end + int(len(df) * validation_frac)

#     # Split the DataFrame
#     train_df = df[:train_end]
#     validation_df = df[train_end:validation_end]
#     test_df = df[validation_end:]

#     return train_df, validation_df, test_df

# train_df, validation_df, test_df = random_split(balanced_df, 0.7, 0.1)
# # Test size is implied to be 0.2 as the remainder

# # train_df.to_csv("train.csv", index=None)
# # validation_df.to_csv("validation.csv", index=None)
# # test_df.to_csv("test.csv", index=None)