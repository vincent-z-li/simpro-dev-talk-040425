from fastapi import APIRouter, HTTPException
from api.models.query_models import QueryRequest, QueryResponse
from api.services.qa_service import answer_with_rag
from api.core.logging import logger

router = APIRouter()

@router.post("/ask", response_model=QueryResponse,
         summary="Answer a Simpro Mobile related question with RAG, using Mobile Help Guide from L&D",
         description="Sends a question to the LLM using Retrieval-Augmented Generation.")
async def ask_question(query: QueryRequest):
    try:
        result = answer_with_rag(query.question, query.structured)
        return result
    except Exception as e:
        logger.error(f"Error in RAG endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")