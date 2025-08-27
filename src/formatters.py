"""
Formateadores para generar salidas en diferentes formatos
"""
from typing import List, Dict, Any
from .models import Issue, ExtendedIssue
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
        md += "| Internal ID - User Id | Título | Responsable | Estado | Estimación | Tiempo gastado | Última actualización | Comentarios |\n"
        md += "|-----------------------|--------|------------|---------|------------|----------------|----------------------|-------------|\n"


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

            md += f"| {task.id} - {task.idReadable} | {task.summary} | {assignee_name} | {state} | {estimation} | {spent} | {time_elapsed} | {comments_text} |\n"

        return md

    @staticmethod
    def format_extended_issue(issue: ExtendedIssue) -> str:
        """
        Formatea una ExtendedIssue para análisis por IA de manera optimizada
        
        Args:
            issue: ExtendedIssue a formatear
            
        Returns:
            str: Información completa en formato markdown optimizado para IA
        """
        
        # Encabezado principal
        md = f"# Issue {issue.idReadable}: {issue.summary}\n\n"
        
        # Información básica en tabla estructurada
        md += "## 📋 Información Básica\n\n"
        md += "| Campo | Valor |\n"
        md += "|-------|-------|\n"
        md += f"| **ID Interno** | {issue.id} |\n"
        md += f"| **ID Legible** | {issue.idReadable} |\n"
        md += f"| **Título** | {issue.summary} |\n"
        md += f"| **Estado** | {issue.state or 'Sin estado'} |\n"
        md += f"| **Prioridad** | {issue.priority or 'Sin prioridad'} |\n"
        md += f"| **Tipo** | {issue.type or 'Sin tipo'} |\n"
        md += f"| **Subsistema** | {issue.subsystem or 'Sin subsistema'} |\n"
        md += f"| **Responsable** | {issue.assignee or 'Sin asignar'} |\n"
        md += f"| **Proyecto** | {issue.project_name or 'Sin proyecto'} |\n"
        
        # Información temporal
        md += "\n## ⏰ Información Temporal\n\n"
        md += "| Campo | Valor |\n"
        md += "|-------|-------|\n"
        
        if issue.created:
            created_elapsed = _calculate_time_elapsed(issue.created)
            md += f"| **Creado** | {created_elapsed} |\n"
        else:
            md += f"| **Creado** | Fecha desconocida |\n"
            
        if issue.updated:
            updated_elapsed = _calculate_time_elapsed(issue.updated)
            md += f"| **Última actualización** | {updated_elapsed} |\n"
        else:
            md += f"| **Última actualización** | Fecha desconocida |\n"
            
        md += f"| **Estimación** | {issue.estimation or 'Sin estimación'} |\n"
        md += f"| **Tiempo gastado** | {issue.spent or 'Sin tiempo registrado'} |\n"
        
        # Personas involucradas
        md += "\n## 👥 Personas Involucradas\n\n"
        md += "| Rol | Persona |\n"
        md += "|-----|----------|\n"
        md += f"| **Reporter** | {issue.reporter_name or 'Desconocido'} |\n"
        md += f"| **Responsable** | {issue.assignee or 'Sin asignar'} |\n"
        md += f"| **Último editor** | {issue.updater_name or 'Desconocido'} |\n"
        
        # Descripción
        if issue.wikifiedDescription:
            md += "\n## 📝 Descripción\n\n"
            md += f"{issue.wikifiedDescription}\n\n"
        
        # Comentarios
        if issue.comments:
            md += f"\n## 💬 Comentarios ({len(issue.comments)})\n\n"
            for i, comment in enumerate(issue.comments, 1):
                md += f"**Comentario {i}:** {comment}\n\n"
        else:
            md += "\n## 💬 Comentarios\n\nSin comentarios.\n\n"
        
        # Relaciones (parent, subtasks, links)
        has_relations = issue.parent or issue.subtasks or issue.links
        if has_relations:
            md += "\n## 🔗 Relaciones\n\n"
            
            if issue.parent:
                md += f"**Issue padre:** {issue.parent}\n\n"
            
            if issue.subtasks:
                md += f"**Subtareas ({len(issue.subtasks)}):**\n"
                for subtask in issue.subtasks:
                    md += f"- {subtask}\n"
                md += "\n"
            
            if issue.links:
                md += f"**Enlaces ({len(issue.links)}):**\n"
                for link in issue.links:
                    md += f"- {link}\n"
                md += "\n"
        
        # Archivos adjuntos
        if issue.attachments:
            md += f"\n## 📎 Archivos Adjuntos ({len(issue.attachments)})\n\n"
            for attachment in issue.attachments:
                md += f"- {attachment}\n"
            md += "\n"
        
        # Tags
        if issue.tags:
            md += f"\n## 🏷️ Tags\n\n"
            tags_text = ", ".join(issue.tags)
            md += f"{tags_text}\n\n"
        
        return md