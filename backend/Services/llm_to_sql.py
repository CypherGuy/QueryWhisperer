import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def text_to_sql(nl_question: str, db_schema: str = "") -> str:
    prompt = (
        "Translate this natural language question to SQL.\n\n"
        f"Schema:\n{db_schema}\n\n"
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
