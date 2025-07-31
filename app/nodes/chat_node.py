from app.models.agent_state import AgentState
from app.chains.chains import get_chat_chain
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from dotenv import load_dotenv
load_dotenv()

def chat_node(state: AgentState) -> AgentState:
    """
    Handles general queries and updates short-term memory manually.
    """

    
    chat_history: list[BaseMessage] = state.get("chat_history") or []

    response = get_chat_chain().invoke({
        "query": state["query"], 
        "chat_history": state["chat_history"]
    }) 

    chat_history.append(AIMessage(content=response.content))
    # chat_history.append({"AI":response.content})
    state["output"] = response.content
    return state