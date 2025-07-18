from app.models.agent_state import AgentState
from app.chains.chains import get_network_designer_chain
from app.models.models import Network_design


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
    Generates a network design from user query.
    Adds the network design to the agent state.
    """

    design_result = get_network_designer_chain().invoke({"query": state["query"]})

    design = Network_design.model_validate(design_result)

    formatted_output = format_network_design(design)

    return {
        **state,
        "network_design": formatted_output

    }