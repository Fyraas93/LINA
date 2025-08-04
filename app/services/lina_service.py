from app.workflow.graph import create_workflow_graph
from dotenv import load_dotenv
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
import os
import uuid
import asyncio
from typing import Optional
from langgraph.checkpoint.memory import InMemorySaver

# Load environment variables
load_dotenv()

# Langfuse setup
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

langfuse_handler = CallbackHandler()


class linaService:
    def __init__(self,memory:InMemorySaver):
        self.memory=memory
        self.workflow_app = create_workflow_graph(self.memory)

    async def lina_invoke(self, query: str, thread_id: Optional[str] = None) -> dict:
        return self.workflow_app.invoke(
            {"query": query},
            config={
                "callbacks": [langfuse_handler],
                "thread_id": "123",
            }
        )
