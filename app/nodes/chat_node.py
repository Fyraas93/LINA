from app.models.agent_state import AgentState
from app.chains.chains import get_chat_chain

def chat_node(state: AgentState) -> AgentState:
    """
    The chat node is responsible for handling general chat queries that fall under the specific tools like log analysis, network design, or server management.
    """

    design = get_chat_chain().invoke({"query": state["query"]})
    return {
        **state,
        "chat_response": design
    }