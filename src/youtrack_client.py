"""
Cliente para la API de YouTrack
"""
import requests
from typing import List, Tuple, Optional
import logging

from .config import YouTrackConfig
from .models import Board, Issue

logger = logging.getLogger("Youtrack MCP")


class YouTrackAPIError(Exception):
    """Excepción específica para errores de la API de YouTrack"""
    pass


class YouTrackClient:
    """Cliente para interactuar con la API de YouTrack"""
    
    def __init__(self, config: YouTrackConfig):
        self.config = config
    
    def get_boards(self) -> Tuple[List[Board], Optional[str]]:
        """
        Obtiene todos los tableros disponibles
        
        Returns:
            Tuple[List[Board], Optional[str]]: Lista de tableros y error si existe
        """
        try:
            fields = "id,name,currentSprint(id,name)"
            url = f"{self.config.base_url}/agiles?fields={fields}"
            
            response = requests.get(url, headers=self.config.headers, timeout=30)
            response.raise_for_status()
            
            boards_data = response.json()
            boards = []
            
            for board_data in boards_data:
                current_sprint = board_data.get('currentSprint')
                board = Board(
                    id=board_data['id'],
                    name=board_data['name'],
                    current_sprint_id=current_sprint['id'] if current_sprint else None,
                    current_sprint_name=current_sprint['name'] if current_sprint else None
                )
                boards.append(board)
            
            return boards, None
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error al obtener tableros: {str(e)}"
            logger.error(error_msg)
            return [], error_msg
        except Exception as e:
            error_msg = f"Error inesperado al obtener tableros: {str(e)}"
            logger.error(error_msg)
            return [], error_msg
    
    def get_sprint_issues(self, board_id: str, sprint_id: str) -> Tuple[List[Issue], Optional[str]]:
        """
        Obtiene las issues de un sprint específico
        
        Args:
            board_id: ID del tablero
            sprint_id: ID del sprint
            
        Returns:
            Tuple[List[Issue], Optional[str]]: Lista de issues y error si existe
        """
        try:
            fields = "id,summary,created,updated,resolved,customFields(id,name,value(name,email,presentation))"
            url = f"{self.config.base_url}/agiles/{board_id}/sprints/{sprint_id}/issues?fields={fields}"
            
            response = requests.get(url, headers=self.config.headers, timeout=30)
            response.raise_for_status()
            
            issues_data = response.json()
            issues = [Issue.from_youtrack_data(issue_data) for issue_data in issues_data]
            
            return issues, None
            
        except requests.exceptions.RequestException as e:
            error_msg = f"Error al obtener issues del sprint {sprint_id}: {str(e)}"
            logger.error(error_msg)
            return [], error_msg
        except Exception as e:
            error_msg = f"Error inesperado al obtener issues: {str(e)}"
            logger.error(error_msg)
            return [], error_msg
    
    def find_board_by_name(self, name: str) -> Tuple[Optional[Board], Optional[str]]:
        """
        Busca un tablero por nombre (coincidencia exacta, case-insensitive)
        
        Args:
            name: Nombre del tablero a buscar
            
        Returns:
            Tuple[Optional[Board], Optional[str]]: Tablero encontrado y error si existe
        """
        boards, error = self.get_boards()
        if error:
            return None, error
        
        # Log de tableros disponibles
        logger.info("Tableros disponibles:")
        for board in boards:
            logger.info(f"{board.id} - {board.name} con sprint: {board.current_sprint_name or 'N/A'}")
        
        # Filtrar por nombre
        matching_boards = [b for b in boards if b.name.strip().lower() == name.strip().lower()]
        
        if not matching_boards:
            available_boards = [b.name for b in boards]
            error_msg = f"No se encontró ningún tablero con el nombre '{name}'. Tableros disponibles: {', '.join(available_boards)}"
            return None, error_msg
        
        if len(matching_boards) > 1:
            board_names = [b.name for b in matching_boards]
            error_msg = f"Se encontraron múltiples tableros con el nombre '{name}': {', '.join(board_names)}"
            return None, error_msg
        
        return matching_boards[0], None
