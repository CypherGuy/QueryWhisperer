from fastapi import APIRouter, Depends, HTTPException

from backend import models
from backend import schemas
from backend import Security
from backend.Services.llm_to_sql import text_to_sql
from backend.routes.auth import get_current_user


router = APIRouter()

DANGEROUS_KEYWORDS: set[str] = {"DROP", "ALTER",
                                "TRUNCATE", "GRANT", "REVOKE", "DELETE"}


def contains_dangerous_sql(sql: str) -> bool:
    return any(word in sql.upper() for word in DANGEROUS_KEYWORDS)


@router.post("/query", response_model=schemas.QueryResponse)
async def nl_to_sql(
    query_request: schemas.QueryRequest,
    current_user: models.User = Depends(get_current_user),
) -> schemas.QueryResponse:
    """Convert a natural language query to a SQL query."""
    # Input validation
    if not query_request.question.strip():
        raise HTTPException(
            status_code=400, detail="Question cannot be empty.")
    if len(query_request.question) > 300:
        raise HTTPException(
            status_code=400, detail="Question too long, your limit is 300 characters.")
    if len(query_request.db_schema) > 10:
        raise HTTPException(
            status_code=400, detail="Too many tables provided, your limit is 10.")

    for table in query_request.db_schema:
        if len(table.columns) > 50:
            raise HTTPException(
                status_code=400,
                detail=f"Too many columns in table '{table.table}', your limit is 50.",
            )
    if current_user.openai_api_key is None:
        raise HTTPException(
            status_code=400,
            detail="No OpenAI API key on file. Please save your key before querying."
        )

    key_to_use: str = (
        query_request.api_key
        or Security.decrypt_api_key(current_user.openai_api_key)
    )

    hashed_email: str = Security.encrypt_email(current_user.email)
    if query_request.api_key and Security.decrypt_email(hashed_email) != current_user.email:
        raise HTTPException(status_code=403, detail="Invalid API key.")

    generated_sql: str = text_to_sql(
        query_request.question,
        [table.model_dump() for table in query_request.db_schema],
        hashed_email,
        key_to_use=key_to_use,

    )

    if contains_dangerous_sql(generated_sql):
        raise HTTPException(
            status_code=400, detail="Query contains disallowed keywords.",
        )

    return schemas.QueryResponse(generated_sql=generated_sql)
