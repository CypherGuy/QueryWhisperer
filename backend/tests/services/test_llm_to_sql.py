from unittest.mock import patch
from backend.Services.llm_to_sql import text_to_sql


class FakeMessage:
    def __init__(self, content):
        self.content = content


class FakeChoice:
    def __init__(self, message):
        self.message = message


class FakeResponse:
    def __init__(self, content):
        self.choices = [FakeChoice(FakeMessage(content))]


@patch("backend.Services.llm_to_sql.client.chat.completions.create")
def test_text_to_sql_returns_sql(mock_create):
    mock_create.return_value = FakeResponse("SELECT * FROM users;")
    question = "Get all users"
    db_schema = [{"table": "users", "columns": ["id", "name", "email"]}]
    sql = text_to_sql(question, db_schema)
    assert isinstance(sql, str)
    assert "SELECT" in sql.upper()


@patch("backend.Services.llm_to_sql.client.chat.completions.create")
def test_text_to_sql_handles_empty_response(mock_create):
    mock_create.return_value = FakeResponse("")
    sql = text_to_sql("Anything", [{"table": "x", "columns": ["y"]}])
    assert sql == "[Error] No SQL response generated."


@patch("backend.Services.llm_to_sql.client.chat.completions.create")
def test_text_to_sql_handles_empty_schema(mock_create):
    mock_create.return_value = FakeResponse("SELECT * FROM unknown;")
    sql = text_to_sql("Something", [])
    assert "SELECT" in sql.upper()


@patch("backend.Services.llm_to_sql.client.chat.completions.create")
def test_text_to_sql_handles_api_failure(mock_create):
    mock_create.side_effect = Exception("API down")
    sql = text_to_sql("Fail case", [{"table": "x", "columns": ["y"]}])
    assert sql.startswith("[Error] Failed to generate SQL")
