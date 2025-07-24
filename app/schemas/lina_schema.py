from pydantic import BaseModel, Field
from typing import Optional, Union
from app.models.models import Log_analysis, Network_design, Server_manager

class QueryResponseUnifiedOutput(BaseModel):
    query: str
    Agent: Optional[str] = None  # Maps internal "supervisor" to "Agent"
    output: Optional[Union[Log_analysis, Network_design, Server_manager, str]] = None

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
