from app.workflow.graph import create_workflow_graph
from langchain_core.messages import HumanMessage, AIMessage
import uuid
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
import os
from dotenv import load_dotenv
from rich import print

load_dotenv()
# Langfuse setup
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

langfuse_handler = CallbackHandler()



# Create the LangGraph workflow
app = create_workflow_graph()

# Start a new session with a unique thread_id
# thread_id = str(uuid.uuid4())
messages = []

# First message
result = app.invoke(
    {
        "query": "Hey my name is firas lakhdher and i'm with my friend ahmed now but i was with ali yesterday",
    },
    config={
        "callbacks": [langfuse_handler],
    }
)
print("Bot:", result["chat_response"])

# Update memory

# Second message in same session
result = app.invoke(
    {
        "query": "What did I say before?",
    },
    config={
        "callbacks": [langfuse_handler],
    }
)
print("Bot:", result["chat_response"])


# Second message in same session
result = app.invoke(
    {
        "query": "Who am i ?",
    },
    config={
        "callbacks": [langfuse_handler],
    }
)
print("Bot:", result["chat_response"])