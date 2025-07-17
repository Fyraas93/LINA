from app.workflow.graph import create_workflow_graph
from dotenv import load_dotenv
load_dotenv()
from langfuse import Langfuse
from langfuse.langchain import CallbackHandler
import os

langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    host=os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

langfuse_handler = CallbackHandler()

class linaService:
    """
    LinaService is a class that provides methods to create and manage the workflow graph for the LINA application.
    It includes methods to create nodes for different functionalities such as log analysis, network design, server management, and chat.
    """

    def lina_invoke(self, query: str):
        """
        Invoke the LINA workflow with a given query.
        
        Args:
            query (str): The user query to be processed by the LINA workflow.
        
        Returns:
            The result of the workflow invocation.
        """
        workflow_app = create_workflow_graph()
        result = workflow_app.invoke({"query": query}, config={"callbacks": [langfuse_handler]})
        return result