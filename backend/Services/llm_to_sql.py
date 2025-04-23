import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def format_schema(tables: list[dict]) -> str:
    return "\n\n".join(
        f"Table: {t['table']}\nColumns: {', '.join(t['columns'])}" for t in tables
    )


def text_to_sql(nl_question: str, db_schema: list[dict]) -> str:
    schema_str = format_schema(db_schema)
    prompt = (
        "Translate this natural language question to SQL. Make the query as simple as possible. I only want the query, no extra messages, speechmarks or backticks.\n\n"
        f"Example output:\nSELECT * FROM users;\n\n"
        f"Schema:\n{schema_str}\n\n"
        f"Question:\n{nl_question}\n\nSQL:"
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[{"role": "user", "content": prompt}]
        )
        message = completion.choices[0].message
        if message and message.content:
            return message.content.strip()
        return "[Error] No SQL response generated."
    except Exception as e:
        return f"[Error] Failed to generate SQL: {str(e)}"
