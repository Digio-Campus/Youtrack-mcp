"""
Servidor MCP para YouTrack
"""
from mcp.server.fastmcp import FastMCP
import logging

from .config import YouTrackConfig
from .youtrack_client import YouTrackClient
from .formatters import MarkdownFormatter

logger = logging.getLogger("Youtrack MCP")

# Create the MCP server instance
mcp = FastMCP("Youtrack MCP Server")
formatter = MarkdownFormatter()

# Variables globales que se inicializarán en run_server()
config = None
client = None


@mcp.tool()
def getTasksInformation(name: str, num_comments: int = 1) -> str:
    """
    Read the Agile Panel from Youtrack, obtaining information about all the tasks and returns a markdown detailing it.

    Args:
        name (str): The name of the board to which the tasks belong.
        num_comments (int): Number of latest comments to retrieve per task (default: 1).

    Returns:
        str: A string containing information about all tasks in markdown format.
    """
    
    # Validar configuración
    if not config or not config.is_configured:
        return "❌ **Error de configuración**\n\nLas variables de entorno YOUTRACK_BASE_URL y YOUTRACK_API_TOKEN deben estar configuradas."
    
    # Validar parámetro num_comments
    if num_comments < 0:
        return "❌ **Error de parámetro**\n\nEl número de comentarios debe ser mayor o igual a 0."
    
    # Buscar tablero por nombre
    board, error = client.find_board_by_name(name)
    if error:
        return f"❌ **Error al buscar tablero**\n\n{error}"
    
    # Verificar que tenga sprint activo
    if not board.current_sprint_id:
        return f"⚠️ **Sin sprint activo**\n\nEl tablero '{board.name}' no tiene un sprint activo."
    
    # Obtener issues del sprint
    issues, error = client.get_sprint_issues(board.id, board.current_sprint_id, num_comments)
    if error:
        return f"❌ **Error al obtener tareas**\n\n{error}"
    
    # Filtrar solo tareas en progreso (no terminadas)
    in_progress_issues = [
        issue for issue in issues 
        if not issue.is_finished(config.finished_states)
    ]
    
    # Log de tareas en progreso
    logger.info("Tareas EN CURSO:")
    for task in in_progress_issues:
        logger.info(f"- {task.id} | {task.summary}")
    
    # Generar el reporte en markdown
    return formatter.format_tasks_report(in_progress_issues)

@mcp.tool()
def getIssueById(issue_id: str) -> str:
    """
    Obtiene información detallada de una issue específica por su ID.
    
    Esta herramienta está diseñada para profundizar en issues problemáticas identificadas
    previamente, proporcionando contexto completo incluyendo todos los comentarios,
    descripción y metadatos para análisis por IA.

    Args:
        issue_id (str): El ID de la issue a analizar (ej: "PROJ-123").

    Returns:
        str: Información completa de la issue en formato markdown estructurado.
    """
    
    # Validar configuración
    if not config or not config.is_configured:
        return "❌ **Error de configuración**\n\nLas variables de entorno YOUTRACK_BASE_URL y YOUTRACK_API_TOKEN deben estar configuradas."
    
    # Validar parámetro issue_id
    if not issue_id or not issue_id.strip():
        return "❌ **Error de parámetro**\n\nEl ID de la issue es requerido y no puede estar vacío."
    
    issue_id = issue_id.strip()
    
    # Obtener issue por ID
    issue, error = client.get_issue_by_id(issue_id)
    if error:
        return f"❌ **Error al obtener issue**\n\n{error}"
    
    if not issue:
        return f"❌ **Issue no encontrada**\n\nNo se pudo obtener la issue con ID '{issue_id}'. Verifica que el ID sea correcto y tengas permisos de acceso."
    
    # Log de la issue obtenida
    logger.info(f"Issue obtenida: {issue.id} | {issue.summary}")
    
    # Generar el reporte detallado en markdown
    return formatter.format_extended_issue(issue)


def run_server(timeout: int = 30, finished_states: str = "Fixed,Verified"):
    """
    Ejecuta el servidor MCP con configuración personalizable
    
    Args:
        timeout: Timeout para requests en segundos
        finished_states: Estados considerados terminados (separados por comas)
    """
    global config, client
    
    # Parsear estados terminados
    parsed_states = [state.strip() for state in finished_states.split(',')]
    
    # Inicializar configuración y cliente una sola vez
    config = YouTrackConfig(timeout=timeout, finished_states=parsed_states)
    client = YouTrackClient(config)
    
    mcp.run(transport="stdio")
