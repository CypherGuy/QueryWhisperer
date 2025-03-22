import torch
import pytest
from embeddings import EmbeddingLayer
from preprocess import vocab_size, dimensions


@pytest.fixture
def embedding_layer():
    return EmbeddingLayer()


def test_embedding_shape(embedding_layer):
    dummy_input = torch.randint(0, vocab_size, (2, 10))
    output = embedding_layer(dummy_input)
    assert output.shape == (2, 10, dimensions)


def test_embedding_type(embedding_layer):
    dummy_input = torch.randint(0, vocab_size, (1, 5))
    output = embedding_layer(dummy_input)
    # Check that the output is a torch.Tensor of floating point type
    assert isinstance(output, torch.Tensor)
    assert output.dtype in [torch.float32, torch.float64]


def test_invalid_token_ids(embedding_layer):
    # Create token IDs that are out of range (e.g., vocab_size, which is invalid because valid IDs are 0 to vocab_size - 1)
    dummy_input = torch.tensor([[0, vocab_size]])
    with pytest.raises(IndexError):
        _ = embedding_layer(dummy_input)


def test_get_embeddings_method(embedding_layer):
    # Ensure get_embeddings() returns an instance of nn.Embedding
    embed_layer = embedding_layer.get_embeddings()
    from torch.nn import Embedding
    assert isinstance(embed_layer, Embedding)
