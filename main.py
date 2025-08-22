# server.py
from mcp.server.fastmcp import FastMCP
import requests
import dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Youtrack MCP")

# Create the MCP server instance
mcp = FastMCP("Youtrack MCP Server")

# Configuración
dotenv.load_dotenv()  # Cargar variables de entorno desde .env
BASE_URL = "https://javilujann.youtrack.cloud/api"
HEADERS = {
    "Authorization": f"Bearer {dotenv.get_key('.env', 'YOUTRACK_API_TOKEN')}",
    "Accept": "application/json"
}

# 1. Listar tableros
def get_boards():
    fields = "id,name,currentSprint(id,name)"
    url = f"{BASE_URL}/agiles?fields={fields}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def filter_boards(name):
    return [b for b in boards if name.lower() in b['name'].lower()]

# 2. Listar sprints de un tablero
def get_sprints(board_id):
    url = f"{BASE_URL}/agiles/{board_id}/sprints?fields=id,name"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

# 3. Obtener issues de un sprint
def get_issues(board_id, sprint_id):
    fields = "id,summary,customFields(id,name,value(name))"
    url = f"{BASE_URL}/agiles/{board_id}/sprints/{sprint_id}/issues?fields={fields}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

# 4. Filtrar tareas "En curso"
def filter_in_progress(issues):
    result = []
    for issue in issues:
        for field in issue.get("customFields", []):
            if field["name"] == "State" and field.get("value", {}).get("name") != "Fixed":
                result.append({
                    "id": issue["id"],
                    "summary": issue["summary"]
                })
    return result

# Timestamp tool
@mcp.tool()
def getTasksInformation() -> str:
    """
    Read the Agile Panel from Youtrack, obtaining information about all the tasks and returns a markdown detailing it.
    
    Returns:
        str: A string containing information about all tasks in markdown format.
    """
    return "Task information in markdown format"



if __name__ == "__main__":
    #mcp.run(transport="stdio")
    boards = get_boards()

    logger.info("Tableros disponibles:")
    for b in boards:
        logger.info(f"{b['id']} - {b['name']} con sprint: {b['currentSprint']['name'] if b.get('currentSprint') else 'N/A'}")

    filtered_boards = filter_boards("Prueba")
    board_id = filtered_boards[0]["id"]  # el primero como ejemplo
    sprints = get_sprints(board_id)
    logger.info("Sprints:")
    for s in sprints:
        logger.info(f"{s['id']} - {s['name']}")

    sprint_id = sprints[0]["id"]  # primer sprint como ejemplo
    issues = get_issues(board_id, sprint_id)
    in_progress = filter_in_progress(issues)

    logger.info("Tareas EN CURSO:")
    for t in in_progress:
        logger.info(f"- {t['id']} | {t['summary']}")
