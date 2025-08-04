from dotenv import load_dotenv
import paramiko
import os
import re
from rich import print
from app.models.agent_state import AgentState
from app.models.models import Server_manager
from app.chains.chains import get_server_manager_chain
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage

load_dotenv()

def remove_sudo(command: str) -> str:
    """
    Removes 'sudo' keyword to ensure root execution without redundant prefix.
    """
    return re.sub(r'\bsudo\b', '', command).strip()

def execute_ssh_command(command: str) -> Server_manager:
    """
    Executes a shell command via SSH and returns the result in Server_manager schema.
    """
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        ssh.connect(
            hostname=os.getenv("SERVER_HOSTNAME"),
            username=os.getenv("SERVER_USERNAME"),  # should be 'root'
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
    Interprets the user query using the LLM, executes the command via SSH,
    and updates the agent state with result and message history.
    """
    user_query = state["query"]
    chat_history: list[BaseMessage] = state.get("chat_history") or []

    # Step 1: Get command from LLM
    command_output = get_server_manager_chain().invoke({"query": user_query})
    raw_command = command_output.command
    cleaned_command = remove_sudo(raw_command)

    print("[bold yellow]LLM raw command:[/bold yellow]", raw_command)
    print("[bold green]Cleaned command:[/bold green]", cleaned_command)

    # Step 2: Execute the command
    result = execute_ssh_command(cleaned_command)

    # Step 3: Update chat history
    chat_history.append(HumanMessage(content=user_query))
    chat_history.append(AIMessage(content=f"Executing: `{result.command}`\n\n"
                                          f"**Output:**\n{result.output or 'None'}\n\n"
                                          f"**Error:**\n{result.error or 'None'}"))

    # Step 4: Update state
    state["chat_history"] = chat_history

    if result.success and not result.output:
        state["output"] = "Command executed successfully"
    elif result.success:
        state["output"] = result.output
    else:
        state["output"] = f"Command failed.\nError: {result.error}"

    return state
