from dataset import split_into_datasets
import numpy as np
from transformers import AutoTokenizer
from typing import Tuple

train_dataset, test_dataset, validation_dataset = split_into_datasets()

tokenizer = AutoTokenizer.from_pretrained("t5-small")
vocab_size = tokenizer.vocab_size
dimensions = 512


def tokenize(text: str) -> Tuple[np.ndarray, np.ndarray]:
    """Tokenizes a given text input into token IDs and attention mask as numpy arrays."""
    encoded = tokenizer(
        text, return_tensors="np", padding="max_length", truncation=True, max_length=64
    )
    return encoded["input_ids"], encoded["attention_mask"]
