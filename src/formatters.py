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
            
            # Usar múltiples comentarios si están disponibles, sino usar last_comment
            if task.comments and len(task.comments) > 0:
                if len(task.comments) == 1:
                    comments_text = task.comments[0]
                else:
                    # Para múltiples comentarios, mostrarlos en líneas separadas
                    comments_text = "<br>".join(task.comments)
            else:
                comments_text = task.last_comment or "Sin comentarios"

            md += f"| {task.id} | {task.summary} | {assignee_name} | {state} | {estimation} | {spent} | {time_elapsed} | {comments_text} |\n"

        return md