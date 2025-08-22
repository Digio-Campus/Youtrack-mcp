"""
Modelos de datos para YouTrack
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


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
    priority: Optional[str] = None
    created: Optional[str] = None
    updated: Optional[str] = None
    
    @classmethod
    def from_youtrack_data(cls, issue_data: Dict[str, Any]) -> 'Issue':
        """Crea una Issue desde los datos de YouTrack"""
        extracted = cls(
            id=issue_data["id"],
            summary=issue_data["summary"],
            created=issue_data.get("created"),
            updated=issue_data.get("updated")
        )
        
        # Extraer campos personalizados
        for field in issue_data.get("customFields", []):
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
            elif field_name == "Priority" and field_value:
                extracted.priority = field_value.get("name")
        
        return extracted
    
    @property
    def is_finished(self) -> bool:
        """Verifica si la issue está terminada"""
        FINISHED_STATES = ["Fixed", "Verified"]
        return self.state in FINISHED_STATES
