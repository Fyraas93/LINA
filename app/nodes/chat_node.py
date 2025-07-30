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
    chat_history.append(HumanMessage(content=state["query"]))

    response = get_chat_chain().invoke(chat_history)

    chat_history.append(AIMessage(content=response.content))
    print('**'*50)
    print("chat_history : ")
    print(chat_history)
    print('**'*50)

    return {
        **state,
        "chat_response": response.content,
        "chat_history": chat_history  # updated memory
    }
