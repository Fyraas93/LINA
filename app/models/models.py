from pydantic import BaseModel, Field
from enum import Enum

class Supervisor_tools(str, Enum):
    ANALYZER = "analyzer_node"
    NETWORK_DESIGNER = "network_designer_node"
    SERVER_MANAGER = "server_manager_node"
    CHAT = "chat_node"
    EXIT = "exit_node"

class Supervisor(BaseModel):
    tool : Supervisor_tools = Field(..., description="""The tool to use for the supervisor node:
                                     - analyzer_node: For log analysis
                                     - network_designer_node: For network design
                                     - server_manager_node: For server management
                                     - chat_node: For general chat and queries
                                     - exit_node: To exit the workflow""")

class Log_analysis(BaseModel):
   # analysis: str = Field(..., description="Detailed analysis of the logs")
   #  serverity: str = Field(..., description="Serverity level of the logs (e.g., low, medium, high)")
   # timestamp: str = Field(..., description="Timestamp of the analysis")
   # summary: str = Field(..., description="Summary of the log analysis")
   # recommendations: list[str] = Field(..., description="List of recommendations based on the log analysis")
    output: str = Field(..., description="Full natural language log analysis report including level summary, frequent errors, issues, summary, and recommendations.")


class Network_design(BaseModel):
    router_config: str
    switch_distribution: str
    ip_addressing: str
    scalability: str
    security: str
    diagram: str
   

class Server_manager(BaseModel):
    command: str = Field(..., description="The shell command executed")
    output: str = Field(..., description="The result of the command")
    success: bool = Field(..., description="True if command executed successfully")
    error: str = Field(..., description="Any error message, if occurred")