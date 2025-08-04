from app.models.agent_state import AgentState
from app.chains.chains import get_network_designer_chain
from app.models.models import Network_design
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

def format_network_design(design: Network_design) -> str:
    return (
        "=== Network Design Report ===\n\n"
        f"Router Configuration:\n{design.router_config}\n\n"
        f"Switch Distribution:\n{design.switch_distribution}\n\n"
        f"IP Addressing Strategy:\n{design.ip_addressing}\n\n"
        f"Scalability Recommendations:\n{design.scalability}\n\n"
        f"Security Recommendations:\n{design.security}\n\n"
        f"Network Topology Diagram:\n{design.diagram}\n"
    )

def network_designer_node(state: AgentState) -> AgentState:
    """
    Generates a network design based on the user's query.
    Stores the formatted result and updates chat history.
    """
    chat_history: list[BaseMessage] = state.get("chat_history") or []

    # Run the chain to get the raw structured output
    design_result = get_network_designer_chain().invoke({"query": state["query"]})

    # Parse the structured result into a Pydantic model
    design = Network_design.model_validate(design_result)

    # Format for presentation
    formatted_output = format_network_design(design)

    # Update chat history
    chat_history.append(HumanMessage(content=state["query"]))
    chat_history.append(AIMessage(content=formatted_output))

    # Update state
    state["output"] = formatted_output
    state["chat_history"] = chat_history

    return state
