from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_message import ChatCompletionMessage

load_dotenv()


def format_schema(tables: list[dict]) -> str:
    return "\n\n".join(
        f"Table: {t['table']}\nColumns: {', '.join(t['columns'])}" for t in tables
    )


def text_to_sql(
    nl_question: str,
    db_schema: list[dict],
    user_hashed_email: str,
    key_to_use: str
) -> str:
    schema_str: str = format_schema(db_schema)
    prompt: str = (
        "Translate this natural language question to SQL. Make the query as simple as possible. "
        "I only want the query, no extra messages, speechmarks or backticks. You must put a semicolon at the end.\n\n"
        f"Example output:\nSELECT * FROM users;\n\n"
        f"Schema:\n{schema_str}\n\n"
        f"Question:\n{nl_question}\n\nSQL:"
    )

    try:
        if not key_to_use:
            return "[Error] No OpenAI API key provided."

        client = OpenAI(api_key=key_to_use)
        completion: ChatCompletion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[{"role": "user", "content": prompt}],
            max_completion_tokens=500,
            n=1,
            user=user_hashed_email)
        message: ChatCompletionMessage = completion.choices[0].message
        if message and message.content:
            return message.content.strip()
        return "[Error] No SQL response generated."

    except OpenAIError as e:
        return f"[Error] OpenAI API failure: {str(e)}"
    except Exception as e:
        return f"[Error] Unexpected failure: {str(e)}"
