"""
Modelos de datos para YouTrack
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from .utils import _calculate_time_elapsed


@dataclass
class Board:
    """Representa un tablero de YouTrack"""
    id: str
    name: str
    current_sprint_id: Optional[str] = None
    current_sprint_name: Optional[str] = None


@dataclass
class Issue:
    """Representa una issue de YouTrack con campos extraídos"""
    id: str
    summary: str
    state: Optional[str] = None
    assignee: Optional[str] = None
    estimation: Optional[str] = None
    spent: Optional[str] = None
    updated: Optional[str] = None
    comments: Optional[List[str]] = None

    # Toda la información para el análisis detallado
    raw_data: Optional[Dict[str, Any]] = None  # Para guardar datos adicionales
    
    @classmethod
    def from_youtrack_data(cls, issue_data: Dict[str, Any], num_comments: int = 1) -> 'Issue':
        """Crea una Issue desde los datos de YouTrack"""
        extracted = cls(
            id=issue_data["id"],
            summary=issue_data["summary"],
            updated=issue_data.get("updated"),
            raw_data=issue_data  # Guardamos todos los datos originales
        )

        # Extracción específica de custom fields
        custom_fields_data = issue_data.get("customFields", [])
        for field in custom_fields_data:
            field_name = field["name"]
            field_value = field.get("value")
            
            if field_name == "State" and field_value:
                extracted.state = field_value.get("name")
            elif field_name == "Assignee" and field_value:
                extracted.assignee = field_value.get("name")
            elif field_name == "Estimation" and field_value:
                extracted.estimation = field_value.get("presentation")
            elif field_name == "Spent time" and field_value:
                extracted.spent = field_value.get("presentation")
        
        # Extraer comentarios
        comments_data = issue_data.get("comments", [])
        if comments_data:
            # Ordenar comentarios por fecha de creación (más reciente primero)
            sorted_comments = sorted(comments_data, key=lambda x: x.get("created", 0), reverse=True)
            
            # Obtener comentarios según num_comments (-1 = todos, >0 = límite)
            if num_comments == -1:
                selected_comments = sorted_comments  # Todos los comentarios
            else:
                selected_comments = sorted_comments[:num_comments]
            
            # Formatear los comentarios
            formatted_comments = []
            for comment in selected_comments:
                comment_text = comment.get("text", "").strip()
                author_name = comment.get("author", {}).get("name", "Desconocido")
                comment_created = comment.get("created")
                elapsed = _calculate_time_elapsed(comment_created) if comment_created else "Desconocido"
                
                if comment_text:
                    formatted_comments.append(f"{author_name}: {comment_text} ({elapsed})")
            
            # Asignar comentarios
            extracted.comments = formatted_comments if formatted_comments else None
        
        return extracted
    
    def is_finished(self, finished_states: List[str]) -> bool:
        """
        Verifica si la issue está terminada
        
        Args:
            finished_states: Lista de estados considerados como terminados
        """
        return self.state in finished_states
