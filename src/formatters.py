"""
Formateadores para generar salidas en diferentes formatos
"""
from typing import List, Dict, Any
from .models import Issue
from .utils import _calculate_time_elapsed


class MarkdownFormatter:
    """Formateador para generar markdown"""
    
    @staticmethod
    def format_tasks_report(issues: List[Issue]) -> str:
        """
        Genera un reporte en markdown de las tareas
        
        Args:
            issues: Lista de issues a formatear
            
        Returns:
            str: Reporte en formato markdown
        """
        if not issues:
            return "# Tareas en curso\n\nNo hay tareas en curso."

        # Generar reporte principal
        md = "# Tareas en curso\n\n"
        md += "| ID | Título | Responsable | Estado | Estimación | Tiempo gastado | Última actualización | Comentarios |\n"
        md += "|-----|--------|------------|---------|------------|----------------|---------------------|-------------|\n"


        for task in issues:
            assignee_name = task.assignee or "Sin asignar"
            estimation = task.estimation or "Sin est."
            spent = task.spent or "Sin tiempo"
            state = task.state or "Sin estado"
            time_elapsed = _calculate_time_elapsed(task.updated) if task.updated else "Desconocido"
            
            # Formatear comentarios
            if task.comments and len(task.comments) > 0:
                if len(task.comments) == 1:
                    comments_text = task.comments[0]
                else:
                    # Para múltiples comentarios, mostrarlos en líneas separadas
                    comments_text = "<br>".join(task.comments)
            else:
                comments_text = "Sin comentarios"

            md += f"| {task.id} | {task.summary} | {assignee_name} | {state} | {estimation} | {spent} | {time_elapsed} | {comments_text} |\n"

        return md

    @staticmethod
    def format_single_issue(issue: Issue) -> str:
        """
        Genera un reporte completo y detallado en markdown de una issue específica
        
        Args:
            issue: Issue a formatear
            
        Returns:
            str: Reporte detallado en formato markdown optimizado para IA
        """
        md = f"# Issue {issue.id}: {issue.summary}\n\n"
        
        # Información básica estructurada
        md += "## Información Básica\n\n"
        md += "| Campo | Valor |\n"
        md += "|-------|-------|\n"
        md += f"| **ID** | {issue.id} |\n"
        md += f"| **Título** | {issue.summary} |\n"
        md += f"| **Estado** | {issue.state or 'Sin estado'} |\n"
        md += f"| **Asignado a** | {issue.assignee or 'Sin asignar'} |\n"
        md += f"| **Prioridad** | {issue.priority or 'Sin prioridad'} |\n"
        md += f"| **Estimación** | {issue.estimation or 'Sin estimación'} |\n"
        md += f"| **Tiempo gastado** | {issue.spent or 'Sin tiempo registrado'} |\n"
        
        # Fechas con tiempo transcurrido
        if issue.created:
            created_elapsed = _calculate_time_elapsed(issue.created)
            md += f"| **Creada** | {created_elapsed} |\n"
        else:
            md += "| **Creada** | Fecha desconocida |\n"
            
        if issue.updated:
            updated_elapsed = _calculate_time_elapsed(issue.updated)
            md += f"| **Última actualización** | {updated_elapsed} |\n"
        else:
            md += "| **Última actualización** | Fecha desconocida |\n"
            
        if issue.resolved:
            resolved_elapsed = _calculate_time_elapsed(issue.resolved)
            md += f"| **Resuelta** | {resolved_elapsed} |\n"
        
        md += "\n"
        
        # Información adicional desde raw_data
        if issue.raw_data:
            raw = issue.raw_data
            
            # Reporter y Updater
            if raw.get("reporter"):
                reporter_name = raw["reporter"].get("name", "Desconocido")
                md += f"| **Reportada por** | {reporter_name} |\n"
            
            if raw.get("updater"):
                updater_name = raw["updater"].get("name", "Desconocido")
                md += f"| **Última actualización por** | {updater_name} |\n"
                
            # Votos y watchers
            if raw.get("votes") is not None:
                md += f"| **Votos** | {raw['votes']} |\n"
                
            if raw.get("watchers"):
                has_star = raw["watchers"].get("hasStar", False)
                md += f"| **Marcada como favorita** | {'Sí' if has_star else 'No'} |\n"
        
        md += "\n"
        
        # Descripción si existe
        if issue.description and issue.description.strip():
            md += "## Descripción\n\n"
            md += f"{issue.description.strip()}\n\n"
        
        # TODOS los Custom Fields
        if issue.all_custom_fields and len(issue.all_custom_fields) > 0:
            md += f"## Campos Personalizados ({len(issue.all_custom_fields)} total)\n\n"
            md += "| Campo | Valor | Tipo | ID |\n"
            md += "|-------|-------|------|----|\n"
            
            for field in issue.all_custom_fields:
                field_name = field.get("name", "Sin nombre")
                field_value = "Sin valor"
                field_type = field.get("type", field.get("$type", "Desconocido"))
                field_id = field.get("id", "Sin ID")
                
                # Formatear el valor según el tipo
                if field.get("value"):
                    value_data = field["value"]
                    if isinstance(value_data, dict):
                        if "name" in value_data:
                            field_value = value_data["name"]
                        elif "presentation" in value_data:
                            field_value = value_data["presentation"]
                        else:
                            field_value = str(value_data)
                    else:
                        field_value = str(value_data)
                
                md += f"| {field_name} | {field_value} | {field_type} | {field_id} |\n"
            
            md += "\n"
        
        # Comentarios detallados
        if issue.comments and len(issue.comments) > 0:
            md += f"## Comentarios ({len(issue.comments)} total)\n\n"
            
            # Revertir orden para mostrar desde el más antiguo al más reciente (cronológico)
            chronological_comments = list(reversed(issue.comments))
            
            for i, comment in enumerate(chronological_comments, 1):
                md += f"### Comentario {i}\n"
                md += f"{comment}\n\n"
        else:
            md += "## Comentarios\n\n"
            md += "No hay comentarios disponibles.\n\n"
        
        # Información adicional desde raw_data
        if issue.raw_data:
            raw = issue.raw_data
            
            # Tags
            if raw.get("tags") and len(raw["tags"]) > 0:
                md += "## Tags\n\n"
                tag_names = [tag.get("name", "Sin nombre") for tag in raw["tags"]]
                md += f"- {', '.join(tag_names)}\n\n"
            
            # Attachments
            if raw.get("attachments") and len(raw["attachments"]) > 0:
                md += f"## Archivos Adjuntos ({len(raw['attachments'])} total)\n\n"
                md += "| Nombre | Tamaño | Tipo | URL |\n"
                md += "|--------|--------|------|-----|\n"
                
                for attachment in raw["attachments"]:
                    name = attachment.get("name", "Sin nombre")
                    size = attachment.get("size", "Desconocido")
                    mime_type = attachment.get("mimeType", "Desconocido")
                    url = attachment.get("url", "Sin URL")
                    
                    md += f"| {name} | {size} bytes | {mime_type} | {url} |\n"
                
                md += "\n"
            
            # Links a otras issues
            if raw.get("links") and len(raw["links"]) > 0:
                md += f"## Enlaces a otras Issues ({len(raw['links'])} total)\n\n"
                
                for link in raw["links"]:
                    direction = link.get("direction", "Desconocido")
                    link_type = link.get("linkType", {}).get("name", "Desconocido")
                    
                    if link.get("issues"):
                        for linked_issue in link["issues"]:
                            issue_id = linked_issue.get("id", "Sin ID")
                            issue_summary = linked_issue.get("summary", "Sin título")
                            md += f"- **{direction}** ({link_type}): {issue_id} - {issue_summary}\n"
                
                md += "\n"
            
            # Visibility/Permisos
            if raw.get("visibility"):
                visibility = raw["visibility"]
                md += "## Visibilidad y Permisos\n\n"
                md += f"- **Tipo**: {visibility.get('type', 'Desconocido')}\n"
                
                if visibility.get("permittedGroups"):
                    groups = [g.get("name", "Sin nombre") for g in visibility["permittedGroups"]]
                    md += f"- **Grupos permitidos**: {', '.join(groups)}\n"
                
                if visibility.get("permittedUsers"):
                    users = [u.get("name", "Sin nombre") for u in visibility["permittedUsers"]]
                    md += f"- **Usuarios permitidos**: {', '.join(users)}\n"
                
                md += "\n"
        
        # Resumen para IA
        md += "## Resumen para Análisis\n\n"
        md += "**Puntos clave a considerar:**\n"
        md += f"- Issue ID: {issue.id}\n"
        md += f"- Estado actual: {issue.state or 'Sin estado'}\n"
        md += f"- Responsable: {issue.assignee or 'Sin asignar'}\n"
        
        if issue.comments:
            md += f"- Total de comentarios: {len(issue.comments)}\n"
            md += "- Actividad de comentarios disponible para análisis temporal\n"
        else:
            md += "- Sin actividad de comentarios registrada\n"
            
        if issue.estimation and issue.spent:
            md += f"- Estimación vs tiempo real: {issue.estimation} / {issue.spent}\n"
        elif issue.estimation:
            md += f"- Estimación sin tiempo registrado: {issue.estimation}\n"
        elif issue.spent:
            md += f"- Tiempo gastado sin estimación inicial: {issue.spent}\n"
        
        if issue.all_custom_fields:
            md += f"- Total de campos personalizados: {len(issue.all_custom_fields)}\n"
            
        if issue.raw_data:
            raw = issue.raw_data
            if raw.get("attachments"):
                md += f"- Archivos adjuntos: {len(raw['attachments'])}\n"
            if raw.get("links"):
                md += f"- Enlaces a otras issues: {len(raw['links'])}\n"
            if raw.get("tags"):
                md += f"- Tags: {len(raw['tags'])}\n"
        
        return md
