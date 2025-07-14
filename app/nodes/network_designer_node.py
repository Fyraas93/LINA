from app.models.agent_state import AgentState
from app.chains.chains import get_network_designer_chain

def network_designer_node(state: AgentState) -> AgentState:
    """
    Generates a network design from user query.
    Adds the network design to the agent state.
    """

    design = get_network_designer_chain().invoke({"query": state["query"]})
    return {
        **state,
        "network_design": design
    }