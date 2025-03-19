import numpy as np
from backend.Model.preprocess import tokenize, vocab_size


def test_tokenize_output_shape():
    """Check the output is the right shape"""
    sample_text = "Get every food item that's at least half off"
    input_ids, attention_mask = tokenize(sample_text)
    # Since max_length is set to 64, expect shapes (1, 64)
    assert input_ids.shape == (1, 64)
    assert attention_mask.shape == (1, 64)


def test_tokenize_valid_ids():
    """Check that all token IDs are valid"""
    sample_text = "This is a test"
    input_ids, _ = tokenize(sample_text)
    assert np.all(input_ids >= 0)
    assert np.all(input_ids < vocab_size)
