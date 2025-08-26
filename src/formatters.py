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
        Genera un reporte detallado en markdown de una issue específica
        
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
        
        md += "\n"
        
        # Descripción si existe
        if issue.description and issue.description.strip():
            md += "## Descripción\n\n"
            md += f"{issue.description.strip()}\n\n"
        
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
        
        return md
