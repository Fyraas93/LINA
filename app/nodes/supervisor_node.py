from app.chains.chains import get_supervisor_chain
from app.models.agent_state import AgentState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from rich import print

def supervisor_node(state: AgentState) -> AgentState:
    """
    Routes the user's query to the appropriate tool by invoking the supervisor chain.
    Updates the agent state with the supervisor's decision and message history.
    """
    # Step 1: Call LLM to classify query into a tool
    supervisor_decision = get_supervisor_chain().invoke({"query": state["query"]})
    selected_tool = supervisor_decision.tool

    print("Supervisor decision:", selected_tool)
    print("Type:", type(selected_tool))

    # Step 2: Update memory
    chat_history = state.get("chat_history",[])
    chat_history.append(HumanMessage(content=state["query"]))
    # chat_history.append({"User":state["query"]})
    chat_history.append(SystemMessage(content=f"Routing query to: `{selected_tool}`"))
    # chat_history.append({"AI":f"Routing query to: `{selected_tool}`"})

    # Step 3: Return updated state
    return {
        **state,
        "supervisor": selected_tool,
        "chat_history": chat_history
    }
