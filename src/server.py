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

# Inicializar configuración y cliente
config = YouTrackConfig()
client = YouTrackClient(config)
formatter = MarkdownFormatter()


@mcp.tool()
def getTasksInformation(name: str) -> str:
    """
    Read the Agile Panel from Youtrack, obtaining information about all the tasks and returns a markdown detailing it.

    Args:
        name (str): The name of the board to which the tasks belong.

    Returns:
        str: A string containing information about all tasks in markdown format.
    """
    
    # Validar configuración
    if not config.is_configured:
        return "❌ **Error de configuración**\n\nLas variables de entorno YOUTRACK_BASE_URL y YOUTRACK_API_TOKEN deben estar configuradas."
    
    # Buscar tablero por nombre
    board, error = client.find_board_by_name(name)
    if error:
        return f"❌ **Error al buscar tablero**\n\n{error}"
    
    # Verificar que tenga sprint activo
    if not board.current_sprint_id:
        return f"⚠️ **Sin sprint activo**\n\nEl tablero '{board.name}' no tiene un sprint activo."
    
    # Obtener issues del sprint
    issues, error = client.get_sprint_issues(board.id, board.current_sprint_id)
    if error:
        return f"❌ **Error al obtener tareas**\n\n{error}"
    
    # Filtrar solo tareas en progreso (no terminadas)
    in_progress_issues = [issue for issue in issues if not issue.is_finished]
    
    # Log de tareas en progreso
    logger.info("Tareas EN CURSO:")
    for task in in_progress_issues:
        logger.info(f"- {task.id} | {task.summary}")
    
    # Generar el reporte en markdown
    return formatter.format_tasks_report(in_progress_issues)


def run_server():
    """Ejecuta el servidor MCP"""
    mcp.run(transport="stdio")
