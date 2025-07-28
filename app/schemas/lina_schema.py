from pydantic import BaseModel
from typing import Optional, Union
from app.models.models import Log_analysis, Network_design, Server_manager

class QueryResponseUnifiedOutput(BaseModel):
    query: str
    Agent: Optional[str] = None  
    output: Optional[Union[Log_analysis, Network_design, Server_manager, str]] = None

    class Config:
        validate_by_name = True
        from_attributes = True


class LinaQueryRequest(BaseModel):
    query: str
    thread_id: Optional[str] = None  