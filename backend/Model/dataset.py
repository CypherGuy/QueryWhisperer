from typing import Tuple
import datasets

dataset = datasets.load_dataset("wikisql")


def split_into_datasets() -> tuple[datasets.Dataset, datasets.Dataset, datasets.Dataset]:
    """Load the WikiSQL dataset from Hugging Face and return train, validation, and test datasets"""
    return dataset["train"], dataset["test"], dataset["validation"]


def extract_question_and_sql(sample: datasets.DatasetDict) -> Tuple[str, str]:
    """Extracts the natural language question and the corresponding SQL query"""
    question_text = sample["question"]
    sql_query = sample["sql"]["human_readable"]
    return question_text, sql_query
