from pydantic import BaseModel, Field

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
