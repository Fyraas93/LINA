from typing import TypedDict, Optional
from langchain_core.messages import BaseMessage
from langchain.schema import Document
from app.models.models import Server_manager

class AgentState(TypedDict):
    query: str
    log_analysis: str | None
    network_design: str | None
    server_manager: Server_manager | None
