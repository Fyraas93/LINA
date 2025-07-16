import paramiko
from app.models.agent_state import AgentState
from app.models.models import Server_manager
from app.chains.chains import get_server_manager_chain
import os
from rich import print

def execute_ssh_command(command: str) -> Server_manager:
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


        hostname = os.getenv("SERVER_HOSTNAME")
        username = os.getenv("SERVER_USERNAME")
        password = os.getenv("SERVER_PASSWORD")
        port =     int(os.getenv("SERVER_PORT"))
        ssh.connect(hostname=hostname, username=username, password=password, port=port)
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode()
        error = stderr.read().decode()

        ssh.close()

        return Server_manager(
            command=command,
            output=output.strip(),
            error=error.strip(),
            success=not bool(error.strip())
        )

    except Exception as e:
        return Server_manager(
            command=command,
            output="",
            error=str(e),
            success=False
        )

def server_manager_node(state: AgentState) -> AgentState:
    user_query = state["query"]
    x = get_server_manager_chain().invoke({"query": user_query})
    print(x)
    command  = x.command
    print("🧠 LLM-generated command:", command)
    result = execute_ssh_command(command)
    
    return {
        **state,
        "server_manager": result
    }
