import torch
import torch.nn as nn
from backend.Model.preprocess import vocab_size, dimensions


class EmbeddingLayer(nn.Module):
    def __init__(self):
        super(EmbeddingLayer, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, dimensions)

    def forward(self, input_ids: torch.Tensor) -> torch.Tensor:
        """Converts a list of token IDs into their corresponding embedding vectors"""
        return self.embeddings(input_ids)

    def get_embeddings(self) -> nn.Embedding:
        """Returns the nn.Embedding layer"""
        return self.embeddings
