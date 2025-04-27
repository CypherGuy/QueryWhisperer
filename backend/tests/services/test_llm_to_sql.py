from dotenv import load_dotenv
import os
from routes.query import contains_dangerous_sql
from unittest.mock import patch
from Services.llm_to_sql import text_to_sql


class FakeMessage:
    def __init__(self, content) -> None:
        self.content = content


class FakeChoice:
    def __init__(self, message) -> None:
        self.message = message


class FakeResponse:
    def __init__(self, content) -> None:
        self.choices: list[FakeChoice] = [FakeChoice(FakeMessage(content))]


load_dotenv(dotenv_path="backend/.env")

key_to_use: str = os.getenv("OPENAI_API_KEY")


@patch("Services.llm_to_sql.client.chat.completions.create")
def test_text_to_sql_returns_sql(mock_create) -> None:
    mock_create.return_value = FakeResponse("SELECT * FROM users;")
    question = "Get all users"
    db_schema = [{"table": "users", "columns": ["id", "name", "email"]}]
    sql = text_to_sql(question, db_schema, key_to_use)
    assert isinstance(sql, str)
    assert "SELECT" in sql.upper()


@patch("Services.llm_to_sql.client.chat.completions.create")
def test_text_to_sql_handles_empty_response(mock_create) -> None:
    mock_create.return_value = FakeResponse("")
    sql = text_to_sql(
        "Anything", [{"table": "x", "columns": ["y"]}], key_to_use)
    assert sql == "[Error] No SQL response generated."


@patch("Services.llm_to_sql.client.chat.completions.create")
def test_text_to_sql_handles_empty_schema(mock_create) -> None:
    mock_create.return_value = FakeResponse("SELECT * FROM unknown;")
    sql = text_to_sql("Something", [], key_to_use)
    assert "SELECT" in sql.upper()


@patch("Services.llm_to_sql.client.chat.completions.create")
def test_text_to_sql_handles_api_failure(mock_create) -> None:
    mock_create.side_effect = Exception("API down")
    sql = text_to_sql(
        "Fail case", [{"table": "x", "columns": ["y"]}], key_to_use)
    assert sql.startswith("[Error] Failed to generate SQL")


def test_contains_dangerous_sql_blocks_drop() -> None:
    assert contains_dangerous_sql("DROP TABLE users;")


def test_contains_dangerous_sql_blocks_alter() -> None:
    assert contains_dangerous_sql("ALTER TABLE orders ADD COLUMN foo INT;")


def test_contains_dangerous_sql_allows_select() -> None:
    assert not contains_dangerous_sql("SELECT * FROM users;")
