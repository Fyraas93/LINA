from typing import TypedDict, Optional, List
from langchain_core.messages import BaseMessage 
from langchain.schema import Document
from app.models.models import Server_manager, Log_analysis, Network_design, Supervisor
from langgraph.prebuilt.chat_agent_executor import AgentState as BaseAgentState

class AgentState(BaseAgentState):  
    query: str
    supervisor: Optional[str]
    log_analysis: Optional[Log_analysis]
    network_design: Optional[str]  
    server_manager: Optional[Server_manager]
    chat_response: Optional[str]
    chat_history: Optional[List[BaseMessage]]
    output : Optional[str]
