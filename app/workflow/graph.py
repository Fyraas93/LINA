from app.nodes.server_manager_node import server_manager_node
from app.nodes.log_analyzer_node import analyzer_node
from app.nodes.network_designer_node import network_designer_node
from app.nodes.supervisor_node import supervisor_node
from app.nodes.chat_node import chat_node
from app.models.models import Supervisor_tools
from langgraph.graph import StateGraph, END, START
from app.models.agent_state import AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver 
import sqlite3

def supervisor_router(state : AgentState):
    router_mapping = {
        Supervisor_tools.ANALYZER: "analyzer_node",
        Supervisor_tools.NETWORK_DESIGNER: "network_designer_node",
        Supervisor_tools.SERVER_MANAGER: "server_manager_node",
        Supervisor_tools.CHAT: "chat_node",
        Supervisor_tools.EXIT: "exit"
    }
    print("*"*50)
    print(state["supervisor"])
    print("*"*50)
    return router_mapping.get(state["supervisor"], None)

def create_workflow_graph():

    print("--"*50)
    print("Creating workflow graph...")
    print("--"*50)
    """
    Create a workflow graph for log analysis, server manager, network designer, and chat.
    """

    graph = StateGraph(AgentState)


    graph.add_node("supervisor_node", supervisor_node)
    graph.add_node("analyzer_node", analyzer_node)
    graph.add_node("network_designer_node", network_designer_node) 
    graph.add_node("server_manager_node", server_manager_node)
    graph.add_node("chat_node", chat_node)

    graph.add_conditional_edges(
        "supervisor_node",
        supervisor_router,
        {
            "analyzer_node": "analyzer_node",
            "network_designer_node": "network_designer_node",
            "server_manager_node": "server_manager_node",
            "chat_node": "chat_node",
            "exit": END
            
        })


    graph.set_entry_point("supervisor_node")
    graph.add_edge("analyzer_node", END)
    graph.add_edge("network_designer_node", END)  
    graph.add_edge("server_manager_node", END)
    graph.add_edge("chat_node", END)

    app = graph.compile()
    app.get_graph().draw_mermaid_png(output_file_path="graph.png")

    return app


    
