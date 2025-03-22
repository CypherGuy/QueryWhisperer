from embeddings import EmbeddingLayer
from preprocess import vocab_size, dimensions, tokenizer, tokenize
import torch
import torch.nn as nn
import torch.nn.functional as F


class Seq2SeqModel(nn.Module):
    def __init__(self, hidden_size: int):
        """
        Initializes a NN as a seq2seq model.

        Args:
            hidden_size (int): The number of features in the hidden state of the LSTMs.
        """
        super(Seq2SeqModel, self).__init__()
        self.embedding = EmbeddingLayer()
        # Encoder: Processes the input embeddings
        self.encoder = nn.LSTM(input_size=dimensions,
                               hidden_size=hidden_size, batch_first=True)
        # Decoder: Generates the output embeddings
        self.decoder = nn.LSTM(input_size=dimensions,
                               hidden_size=hidden_size, batch_first=True)
        # Output layer: Turns decoder to logits
        self.fc_out = nn.Linear(hidden_size, vocab_size)

    def forward(self, src_ids: torch.Tensor, tgt_ids: torch.Tensor) -> torch.Tensor:
        """
        Performs a forward pass of the seq2seq model.
        """
        src_emb = self.embedding(src_ids)
        tgt_emb = self.embedding(tgt_ids)

        # Get the final hidden and cell states from the encoder
        _, (hidden, cell) = self.encoder(src_emb)

        decoder_outputs, _ = self.decoder(tgt_emb, (hidden, cell))

        logits = self.fc_out(decoder_outputs)
        return logits
