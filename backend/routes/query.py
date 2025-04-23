from fastapi import APIRouter
from backend import schemas
from backend.Services.llm_to_sql import text_to_sql

router = APIRouter()


@router.post("/query", response_model=schemas.QueryResponse)
async def query_nl_to_sql(request: schemas.QueryRequest):
    sql = text_to_sql(request.question, [
                      t.model_dump() for t in request.db_schema])
    return schemas.QueryResponse(generated_sql=sql)
