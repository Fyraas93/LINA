from app.workflow.graph import create_workflow_graph
from rich import print
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    workflow_app = create_workflow_graph()
    # You can now run the workflow app with an initial state
    result = workflow_app.invoke({"query": "Show nginx status"})
    print(result)
