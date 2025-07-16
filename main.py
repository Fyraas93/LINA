from app.workflow.graph import create_workflow_graph
from rich import print
from dotenv import load_dotenv
load_dotenv()
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
import os
if __name__ == "__main__":

    langfuse = Langfuse(
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
    )

    langfuse_handler = CallbackHandler()

    workflow_app = create_workflow_graph()
    # You can now run the workflow app with an initial state
    query = input("Enter your query: ")
    result = workflow_app.invoke({"query": query}, config={"callbacks": [langfuse_handler]})
    print(result)
