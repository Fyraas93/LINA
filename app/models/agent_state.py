from typing import TypedDict, Optional
from langchain_core.messages import BaseMessage
from langchain.schema import Document
from app.models.models import Server_manager, Log_analysis, Network_design, Supervisor

class AgentState(TypedDict):
    query: str
    supervisor: str | None
    log_analysis: Log_analysis | None
    network_design: Network_design | None
    server_manager: Server_manager | None
    chat_response: str | None
