from fastapi import APIRouter, HTTPException
from api.models.query_models import QueryRequest, QueryResponse
from api.services.qa_service import answer_non_rag
from api.core.logging import logger

router = APIRouter()

@router.post("/ask", response_model=QueryResponse, 
         summary="Answer a Simpro Mobile related question without RAG",
         description="Sends a question directly to the OpenAI.")
async def ask_question(query: QueryRequest):
    try:
        answer = answer_non_rag(query.question, query.structured)
        return answer;
    except Exception as e:
        logger.error(f"Error in non-RAG endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")