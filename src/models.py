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
    idReadable: str
    summary: str
    state: Optional[str] = None
    assignee: Optional[str] = None
    estimation: Optional[str] = None
    spent: Optional[str] = None
    updated: Optional[str] = None
    comments: Optional[List[str]] = None
    
    @classmethod
    def get_api_fields(cls) -> str:
        """Devuelve los campos necesarios para consultas básicas de Issue"""
        return "id,idReadable,summary,updated,customFields(name,value),comments(author(name),text,created)"
    
    @classmethod
    def from_youtrack_data(cls, issue_data: Dict[str, Any], num_comments: int = 1) -> 'Issue':
        """Crea una Issue desde los datos de YouTrack"""
        extracted = cls(
            id=issue_data["id"],
            idReadable=issue_data["idReadable"],
            summary=issue_data["summary"],
            updated=issue_data.get("updated")
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

@dataclass
class ExtendedIssue(Issue):
    """Representa una issue de YouTrack con información completa para análisis detallado"""
    # Campos procesados (ya extraídos para fácil acceso)
    attachments: Optional[List[str]] = None  # Lista de nombres de archivos
    created: Optional[str] = None  # Timestamp como string
    links: Optional[List[str]] = None  # Descripciones de enlaces procesadas
    parent: Optional[str] = None  # Descripción del padre procesada
    project_name: Optional[str] = None  # Nombre del proyecto extraído
    reporter_name: Optional[str] = None  # Nombre del reporter extraído
    subtasks: Optional[List[str]] = None  # Descripciones de subtasks procesadas
    tags: Optional[List[str]] = None  # Lista de nombres de tags
    updater_name: Optional[str] = None  # Nombre del updater extraído
    wikifiedDescription: Optional[str] = None
    
    @classmethod
    def get_api_fields(cls) -> str:
        """Devuelve los campos completos necesarios para análisis detallado"""
        # Comenzamos con los campos básicos de la clase padre
        basic_fields = super().get_api_fields()
        
        # Agregamos los campos específicos de ExtendedIssue
        extended_fields = (
            "created,wikifiedDescription,"
            "attachments(name),"
            "links(direction,linkType(name),issues(id,idReadable,summary)),"
            "parent(issues(id,idReadable,summary)),"
            "subtasks(issues(id,idReadable,summary,resolved)),"
            "project(id,name),"
            "reporter(name,email),"
            "updater(name,email),"
            "tags(name)"
        )
        
        return f"{basic_fields},{extended_fields}"
    
    @classmethod
    def from_youtrack_data(cls, issue_data: Dict[str, Any], num_comments: int = -1) -> 'ExtendedIssue':
        """Crea una ExtendedIssue desde los datos completos de YouTrack"""
        # Primero creamos la issue básica
        basic_issue = super().from_youtrack_data(issue_data, num_comments)
        
        # Procesamos los campos específicos de ExtendedIssue
        # Attachments: extraer solo nombres
        attachments_processed = None
        if issue_data.get("attachments"):
            attachments_processed = [att.get("name", "Sin nombre") for att in issue_data["attachments"]]
        
        # Links: formatear enlaces de forma legible
        links_processed = None
        if issue_data.get("links"):
            links_processed = []
            for link in issue_data["links"]:
                direction = link.get("direction", "")
                link_type = link.get("linkType", {}).get("name", "relacionado")
                issues = link.get("issues", [])
                
                if issues:
                    issues_desc = ", ".join([f"{issue.get('idReadable', issue.get('id', '?'))}: {issue.get('summary', 'Sin título')}" for issue in issues])
                    links_processed.append(f"{direction} {link_type} → {issues_desc}")
        
        # Parent: formatear información del padre
        parent_processed = None
        if issue_data.get("parent"):
            parent_issues = issue_data["parent"].get("issues", [])
            if parent_issues:
                parent_issue = parent_issues[0]  # Tomamos el primer padre
                parent_processed = f"{parent_issue.get('idReadable', parent_issue.get('id', '?'))}: {parent_issue.get('summary', 'Sin título')}"
        
        # Subtasks: formatear subtareas
        subtasks_processed = None
        if issue_data.get("subtasks"):
            subtasks_processed = []
            for subtask in issue_data["subtasks"]:
                subtask_issues = subtask.get("issues", [])
                for issue in subtask_issues:
                    resolved_status = " (RESUELTO)" if issue.get("resolved") else ""
                    subtasks_processed.append(f"{issue.get('idReadable', issue.get('id', '?'))}: {issue.get('summary', 'Sin título')}{resolved_status}")
        
        # Project: extraer nombre
        project_name = None
        if issue_data.get("project"):
            project_name = issue_data["project"].get("name")
        
        # Reporter: extraer nombre
        reporter_name = None
        if issue_data.get("reporter"):
            reporter_name = issue_data["reporter"].get("name")
        
        # Updater: extraer nombre
        updater_name = None
        if issue_data.get("updater"):
            updater_name = issue_data["updater"].get("name")
        
        # Tags: extraer nombres
        tags_processed = None
        if issue_data.get("tags"):
            tags_processed = [tag.get("name") for tag in issue_data["tags"] if tag.get("name")]
        
        # Crear ExtendedIssue con datos procesados
        extended = cls(
            # Campos heredados de Issue
            id=basic_issue.id,
            idReadable=basic_issue.idReadable,
            summary=basic_issue.summary,
            state=basic_issue.state,
            assignee=basic_issue.assignee,
            estimation=basic_issue.estimation,
            spent=basic_issue.spent,
            updated=basic_issue.updated,
            comments=basic_issue.comments,
            
            # Campos específicos de ExtendedIssue (procesados)
            attachments=attachments_processed,
            created=issue_data.get("created"),
            links=links_processed,
            parent=parent_processed,
            project_name=project_name,
            reporter_name=reporter_name,
            subtasks=subtasks_processed,
            tags=tags_processed,
            updater_name=updater_name,
            wikifiedDescription=issue_data.get("wikifiedDescription")
        )
        
        return extended
