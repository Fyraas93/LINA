from app.models.agent_state import AgentState
from app.chains.chains import get_chat_chain
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from dotenv import load_dotenv
load_dotenv()

def chat_node(state: AgentState) -> AgentState:
    """
    Handles general queries and updates short-term memory manually.
    """

    
    messages: list[BaseMessage] = state.get("messages", []) or []

    
    messages.append(HumanMessage(content=state["query"]))

    response = get_chat_chain().invoke(messages)

  
    messages.append(AIMessage(content=response.content))

    return {
        **state,
        "chat_response": response.content,
        "messages": messages  # updated memory
    }
