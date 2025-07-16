from app.chains.chains import get_supervisor_chain
from app.models.agent_state import AgentState
from rich import print

def supervisor_node(state: AgentState) -> AgentState:
    """
    Routes the user's query to the appropriate node based on the supervisor's decision.
    Adds the supervisor's decision to the agent state.
    """

    # Get the supervisor's decision using the chain
    supervisor_decision = get_supervisor_chain().invoke({"query": state["query"]})

    print("🧠 Supervisor's decision:", supervisor_decision.tool)
    print("type :", type(supervisor_decision.tool))
    return {
        **state,
        "supervisor": supervisor_decision.tool
    }


