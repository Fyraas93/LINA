from dotenv import load_dotenv
import paramiko
import os
from rich import print
from app.models.agent_state import AgentState
from app.models.models import Server_manager
from app.chains.chains import get_server_manager_chain
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

def execute_ssh_command(command: str) -> Server_manager:
    """
    Executes a shell command on a remote server via SSH and returns structured output.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=os.getenv("SERVER_HOSTNAME"),
            username=os.getenv("SERVER_USERNAME"),
            password=os.getenv("SERVER_PASSWORD"),
            port=int(os.getenv("SERVER_PORT"))
        )

        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        ssh.close()

        return Server_manager(
            command=command,
            output=output,
            error=error,
            success=not bool(error)
        )

    except Exception as e:
        return Server_manager(
            command=command,
            output="",
            error=str(e),
            success=False
        )


def server_manager_node(state: AgentState) -> AgentState:
    """
    Interprets a user request into a server command, executes it over SSH,
    and returns the result.
    """

    user_query = state["query"]

    # Step 1: Use LLM to convert query to command
    command_output = get_server_manager_chain().invoke({"query": user_query})
    command = command_output.command

    print("LLM-generated command:", command)

    # Step 2: Run command via SSH
    result = execute_ssh_command(command)

    # Step 3: Update message history if tracking
    messages = state.get("messages", [])
    messages.append(HumanMessage(content=f"Execute server command: {user_query}"))
    messages.append(AIMessage(content=f"Command: `{result.command}`\n\nOutput:\n{result.output}\n\nError:\n{result.error or 'None'}"))

    return {
        **state,
        "server_manager": result,
        "messages": messages
    }
