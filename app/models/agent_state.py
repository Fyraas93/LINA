from typing import TypedDict, Optional
from langchain_core.messages import BaseMessage
from langchain.schema import Document

class AgentState(TypedDict):
    query: str
    log_analysis: str | None
    network_design: str | None