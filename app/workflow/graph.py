from app.nodes.server_manager_node import server_manager_node
from app.nodes.log_analyzer_node import analyzer_node
from app.nodes.network_designer_node import network_designer_node
from langgraph.graph import StateGraph, END, START
from app.models.agent_state import AgentState
 
def create_workflow_graph():
    """
    Create a workflow graph for log analysis and network designer.
    """

    graph = StateGraph(AgentState)

    graph.add_node("analyzer_node", analyzer_node)
    graph.add_node("network_designer_node", network_designer_node) 
    graph.add_node("server_manager_node", server_manager_node)

    graph.set_entry_point("server_manager_node")
  
    graph.add_edge("analyzer_node", END)
    graph.add_edge("network_designer_node", END)  
    graph.add_edge("server_manager_node", END)

    app = graph.compile()
   
    return app
