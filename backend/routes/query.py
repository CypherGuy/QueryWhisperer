from fastapi import APIRouter
from backend import schemas
from backend.Services.llm_to_sql import text_to_sql

router = APIRouter()


@router.post("/query")
async def query_nl_to_sql(request: schemas.QueryRequest):
    sql = text_to_sql(request.question, request.db_schema)
    return {"generated_sql": sql}
