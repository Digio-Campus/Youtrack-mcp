# server.py
from mcp.server.fastmcp import FastMCP
import requests
import os
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Youtrack MCP")

# Create the MCP server instance
mcp = FastMCP("Youtrack MCP Server")

# Configuración - Variables de entorno del sistema
BASE_URL = os.getenv('YOUTRACK_BASE_URL')
API_TOKEN = os.getenv('YOUTRACK_API_TOKEN')

# Validar que las variables de entorno estén configuradas
if not BASE_URL:
    logger.error("Variable de entorno YOUTRACK_BASE_URL no configurada")
if not API_TOKEN:
    logger.error("Variable de entorno YOUTRACK_API_TOKEN no configurada")

# Normalizar BASE_URL
if BASE_URL:
    BASE_URL = BASE_URL.rstrip('/')

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Accept": "application/json"
} if API_TOKEN else {}

# 1. Listar tableros
def get_boards():
    try:
        fields = "id,name,currentSprint(id,name)"
        url = f"{BASE_URL}/agiles?fields={fields}"
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.RequestException as e:
        error_msg = f"Error al obtener tableros: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_msg = f"Error inesperado al obtener tableros: {str(e)}"
        logger.error(error_msg)
        return None, error_msg

# 2. Filtrar tableros por nombre (coincidencia exacta, ignorando mayúsculas/minúsculas)
def filter_boards(boards, name):
    return [b for b in boards if b['name'].strip().lower() == name.strip().lower()]

# 3. Obtener issues de un sprint
def get_issues(board_id, sprint_id):
    try:
        fields = "id,summary,created,updated,resolved,customFields(id,name,value(name,email,presentation))"
        url = f"{BASE_URL}/agiles/{board_id}/sprints/{sprint_id}/issues?fields={fields}"
        r = requests.get(url, headers=HEADERS, timeout=30)
        r.raise_for_status()
        return r.json(), None
    except requests.exceptions.RequestException as e:
        error_msg = f"Error al obtener issues del sprint {sprint_id}: {str(e)}"
        logger.error(error_msg)
        return None, error_msg
    except Exception as e:
        error_msg = f"Error inesperado al obtener issues: {str(e)}"
        logger.error(error_msg)
        return None, error_msg

# 4. Extraer información de campos personalizados de una issue
def extract_issue_fields(issue):
    """
    Extrae y decodifica los campos personalizados de una issue de YouTrack.
    
    Args:
        issue (dict): Issue de YouTrack con customFields
        
    Returns:
        dict: Diccionario con los campos extraídos
    """
    extracted = {
        "id": issue["id"],
        "summary": issue["summary"],
        "state": None,
        "assignee": None,
        "estimation": None,
        "spent": None,
        "priority": None,
        "created": issue.get("created"),
        "updated": issue.get("updated")
    }
    
    for field in issue.get("customFields", []):
        if field["name"] == "State":
            extracted["state"] = field.get("value", {}).get("name")
        elif field["name"] == "Assignee":
            extracted["assignee"] = field.get("value")
        elif field["name"] == "Estimation":
            extracted["estimation"] = field.get("value", {}).get("presentation") if field.get("value") else None
        elif field["name"] == "Spent time":
            extracted["spent"] = field.get("value", {}).get("presentation") if field.get("value") else None
        elif field["name"] == "Priority":
            extracted["priority"] = field.get("value", {}).get("name") if field.get("value") else None
    
    return extracted

# 5. Filtrar tareas "En curso"
def filter_in_progress(issues):
    """
    Filtra las issues que están en progreso (no terminadas).
    
    Args:
        issues (list): Lista de issues de YouTrack
        
    Returns:
        list: Lista de issues en progreso con información estructurada
    """
    # Estados que consideramos "terminados"
    FINISHED_STATES = ["Fixed", "Verified"]
    
    result = []
    for issue in issues:
        extracted_issue = extract_issue_fields(issue)
        
        # Solo incluir tareas que NO estén terminadas
        if extracted_issue["state"] not in FINISHED_STATES:
            result.append(extracted_issue)
    
    return result

def generateMarkdown(issues : list) -> str:
    """
    Genera un markdown con información de las tareas en progreso.
    
    Args:
        issues (list): Lista de issues de YouTrack
        
    Returns:
        str: Markdown con el reporte de tareas
    """
    if not issues:
        return "# Tareas en curso\n\nNo hay tareas en curso."

    # Encabezado del markdown
    md = "# Tareas en curso\n\n"
    md += "| ID | Título | Responsable | Estado | Estimación | Tiempo gastado |\n"
    md += "|-----|--------|------------|---------|------------|----------------|\n"
    
    for task in issues:
        assignee_name = task["assignee"]["name"] if task["assignee"] else "Sin asignar"
        estimation = task["estimation"] or "Sin est."
        spent = task["spent"] or "Sin tiempo"
        state = task["state"] or "Sin estado"
        
        md += f"| {task['id']} | {task['summary']} | {assignee_name} | {state} | {estimation} | {spent} |\n"
    
    return md


# Timestamp tool
@mcp.tool()
def getTasksInformation(name : str) -> str:
    """
    Read the Agile Panel from Youtrack, obtaining information about all the tasks and returns a markdown detailing it.

    Args:
        name (str): The name of the board to which the tasks belong.

    Returns:
        str: A string containing information about all tasks in markdown format.
    """
    
    # Validar configuración
    if not BASE_URL or not API_TOKEN:
        return "❌ **Error de configuración**\n\nLas variables de entorno YOUTRACK_BASE_URL y YOUTRACK_API_TOKEN deben estar configuradas."
    
    # Obtener todos los tableros
    boards, error = get_boards()
    if error:
        return f"❌ **Error al obtener tableros**\n\n{error}"
    
    logger.info("Tableros disponibles:")
    for b in boards:
        logger.info(f"{b['id']} - {b['name']} con sprint: {b['currentSprint']['name'] if b.get('currentSprint') else 'N/A'}")

    # Filtrar tableros por nombre, para obtener el tablero deseado
    filtered_boards = filter_boards(boards, name)
    if not filtered_boards:
        available_boards = [b['name'] for b in boards]
        return f"❌ **Tablero no encontrado**\n\nNo se encontró ningún tablero con el nombre '{name}'.\n\n**Tableros disponibles:**\n" + "\n".join([f"- {board}" for board in available_boards])

    if len(filtered_boards) > 1:
        board_names = [b['name'] for b in filtered_boards]
        return f"⚠️ **Múltiples tableros encontrados**\n\nSe encontraron múltiples tableros con el nombre '{name}':\n" + "\n".join([f"- {board}" for board in board_names])

    board = filtered_boards[0]
    
    # Obtener las issues del sprint actual
    board_id = board['id']
    sprint_id = board['currentSprint']['id'] if board.get('currentSprint') else None
    if not sprint_id:
        return f"⚠️ **Sin sprint activo**\n\nEl tablero '{board['name']}' no tiene un sprint activo."

    issues, error = get_issues(board_id, sprint_id)
    if error:
        return f"❌ **Error al obtener tareas**\n\n{error}"

    # Quedarse solo con las tareas no terminadas
    in_progress = filter_in_progress(issues)

    logger.info("Tareas EN CURSO:")
    for t in in_progress:
        logger.info(f"- {t['id']} | {t['summary']}")

    # Generar el markdown
    return generateMarkdown(in_progress)



if __name__ == "__main__":
    mcp.run(transport="stdio")
