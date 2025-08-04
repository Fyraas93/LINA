from app.models.agent_state import AgentState
from app.chains.chains import get_analyzer_chain
from app.Milvus.Milvus import MilvusStorage
from app.Milvus.embedder import LogEmbedder
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage

load_dotenv()

embedder = LogEmbedder()
milvus_storage = MilvusStorage()

def format_logs_as_text(logs: list[dict]) -> str:
    """
    Convert structured logs into a plain text block to match prompt expectations.
    """
    if not logs:
        return "No logs retrieved from storage."

    formatted_logs = []
    for log in logs:
        formatted_logs.append(
            f"[{log.get('timestamp', 'unknown')}] [{log.get('source', 'unknown')}] "
            f"[{log.get('severity', 'INFO')}] - {log.get('log_message', '')}"
        )
    return "\n".join(formatted_logs)

def analyzer_node(state: AgentState) -> AgentState:
    """
    Analyze logs based on the query and update the agent state with the result.
    """
    chat_history: list[BaseMessage] = state.get("chat_history") or []

    # Retrieve relevant logs from Milvus
    logs = milvus_storage.search_similar_logs(
        query_embedding=embedder.generate_embedding(state["query"]),
        top_k=10
    )
    print("Logs received by analyzer:", logs)

    # Format logs for the LLM
    formatted_logs = format_logs_as_text(logs)

    # Get analysis from the LLM
    analysis = get_analyzer_chain().invoke({
        "query": state["query"],
        "logs": formatted_logs
    })

    # Update chat history
    chat_history.append(HumanMessage(content=state["query"]))
    chat_history.append(AIMessage(content=analysis.output))

    # Update state
    state["output"] = analysis.output
    state["chat_history"] = chat_history

    return state
