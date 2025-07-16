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
    # the log analysis class is the structured output of the llm, this should return useful informations, the input will be bunch of logs to analyze
    analysis: str = Field(..., description="Detailed analysis of the logs")
    serverity: str = Field(..., description="Serverity level of the logs (e.g., low, medium, high)")
    timestamp: str = Field(..., description="Timestamp of the analysis")
    summary: str = Field(..., description="Summary of the log analysis")
    recommendations: list[str] = Field(..., description="List of recommendations based on the log analysis")


class Network_design(BaseModel):
    router_config: str = Field(..., description="Router configuration and placement recommendations")
    switch_distribution: str = Field(..., description="Switch placement and traffic segmentation strategy")
    ip_addressing: str = Field(..., description="Subnetting and IP addressing strategy")
    scalability: str = Field(..., description="Recommendations for scalability and future expansion")
    security: str = Field(..., description="Recommendations for VLANs, firewalls, and failover strategies")
    diagram: str = Field(..., description="ASCII representation of the network topology")


class Server_manager(BaseModel):
    command: str = Field(..., description="The shell command executed")
    output: str = Field(..., description="The result of the command")
    success: bool = Field(..., description="True if command executed successfully")
    error: str = Field(..., description="Any error message, if occurred")