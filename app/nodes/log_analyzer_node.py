from app.models.agent_state import AgentState
from app.chains.chains import get_analyzer_chain
from app.Milvus.Milvus import MilvusStorage
from app.Milvus.embedder import LogEmbedder
from dotenv import load_dotenv
load_dotenv()

embedder = LogEmbedder()
milvus_storage = MilvusStorage()

  
def analyzer_node(state: AgentState) -> AgentState:
    """
    Generate a learning roadmap based on the user's query.
    Adds the analysis to the agent state.
    """

    logs = milvus_storage.search_similar_logs(
        query_embedding=embedder.generate_embedding(state["query"]))
    analysis = get_analyzer_chain().invoke({"query": state["query"], "logs": logs})
    # print(f"🧠 Analysis: {analysis}")
    return {
        **state,
        "log_analysis": analysis  
    }