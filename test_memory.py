from app.workflow.graph import create_workflow_graph
from langchain_core.messages import HumanMessage, AIMessage
import uuid

# Create the LangGraph workflow
app = create_workflow_graph()

# Start a new session with a unique thread_id
thread_id = str(uuid.uuid4())
messages = []

# First message
result = app.invoke(
    {
        "query": "Hey this is lakhdher",
        "messages": messages
    },
    config={"thread_id": thread_id}
)
print("Bot:", result["chat_response"])

# Update memory
messages = result["messages"]

# Second message in same session
result = app.invoke(
    {
        "query": "What did I say before?",
        "messages": messages
    },
    config={"thread_id": thread_id}
)
print("Bot:", result["chat_response"])
