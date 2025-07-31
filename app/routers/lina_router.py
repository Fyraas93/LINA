from fastapi import APIRouter, Body
from app.schemas.lina_schema import QueryResponseUnifiedOutput, LinaQueryRequest
from app.services.lina_service import linaService

router = APIRouter(prefix="", tags=["LINA"])
lina_service = linaService()


@router.get("/health")
async def health_check():
    return {"message": "LINA service is healthy"}


@router.post("/query", response_model=QueryResponseUnifiedOutput)
async def query_lina(query: str = Body(..., embed=True)):
    result = await lina_service.lina_invoke(query)

    agent = result.get("supervisor")
    output = None
    
    if result.get("server_manager"):
       
        output = result["server_manager"].output
    elif result.get("log_analysis"):
        output = result["log_analysis"]
    elif result.get("network_design"):
        output = result["network_design"]
    elif result.get("chat_response"):
        output = {"output": result["chat_response"]}
    else:
        output = {"output": "No output was generated."}

    return QueryResponseUnifiedOutput(
        query=result.get("query", ""),
        Agent=agent,
        output=output
    )


@router.post("/query/session", response_model=QueryResponseUnifiedOutput)
async def query_lina_with_session(payload: LinaQueryRequest):
    result = await lina_service.lina_invoke(payload.query, payload.thread_id)

    agent = result.get("supervisor")
    output = (
        result.get("log_analysis")
        or result.get("network_design")
        or result.get("server_manager")
        or result.get("chat_response")
        or "No output was generated."
    )

    return QueryResponseUnifiedOutput(
        query=result.get("query", ""),
        Agent=agent,
        output=output
    )
