from app.models.agent_state import AgentState
from app.chains.chains import get_analyzer_chain
from app.Milvus.Milvus import MilvusStorage
from app.Milvus.embedder import LogEmbedder
from dotenv import load_dotenv
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
    Generate a learning roadmap based on the user's query.
    Adds the analysis to the agent state.
    """

    logs = milvus_storage.search_similar_logs(
        query_embedding=embedder.generate_embedding(state["query"]), top_k=10)
   
    formatted_logs = format_logs_as_text(logs)

    analysis = get_analyzer_chain().invoke({"query": state["query"], "logs": formatted_logs})
    # print(f"🧠 Analysis: {analysis}")
    return {
        **state,
        "log_analysis": analysis.output  
    }