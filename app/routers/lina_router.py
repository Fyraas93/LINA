from fastapi import APIRouter
from app.schemas.lina_schema import QueryResponseUnifiedOutput
from app.services.lina_service import linaService

router = APIRouter(prefix="", tags=["LINA"])
lina_service = linaService()

@router.get("/health")
async def health_check():
    return {"message": "LINA service is healthy"}

@router.post("/query", response_model=QueryResponseUnifiedOutput)
async def query_lina(query: str):
    result = lina_service.lina_invoke(query)

    # Extract the "supervisor" field and rename to "Agent"
    agent = result.get("supervisor", None)

    # Extract the actual output from possible keys
    output = (
        result.get("log_analysis") or
        result.get("network_design") or
        result.get("server_manager") or
        result.get("chat_response") or
        None
    )

    # Return wrapped response with alias keys
    return QueryResponseUnifiedOutput(query=result.get("query", ""), Agent=agent, output=output)
