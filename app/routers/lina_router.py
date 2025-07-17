from fastapi import APIRouter
from app.schemas.lina_schema import QueryResponse
from app.services.lina_service import linaService

router = APIRouter(prefix="", tags=["LINA"])
lina_service = linaService()

@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify if the LINA service is running.
    
    Returns:
        str: A message indicating the service is healthy.
    """
    return {"message": "LINA service is healthy"}

@router.post("/query")
async def query_lina(query: str):
    """
    Endpoint to query the LINA application.
    
    Args:
        query (str): The user query to be processed by the LINA workflow.
    
    Returns:
        QueryResponse: The response containing the results of the query.
    """
    result = lina_service.lina_invoke(query)
    return result