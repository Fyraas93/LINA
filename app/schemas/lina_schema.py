from pydantic import BaseModel
from typing import Optional
from app.models.models import Log_analysis, Network_design, Server_manager

class UserRequest(BaseModel):
    query: str
    


class QueryResponse(BaseModel):
    query: str
    supervisor: str | None
    log_analysis: Optional[Log_analysis]
    network_design: Optional[Network_design]
    server_manager: Optional[Server_manager]
    chat_response: Optional[str]