"""
Formateadores para generar salidas en diferentes formatos
"""
from typing import List, Dict, Any
from .models import Issue
from datetime import datetime, timezone


def _calculate_time_elapsed(timestamp: str) -> str:
    """
    Calcula el tiempo transcurrido desde un timestamp hasta ahora
    
    Args:
        timestamp: Timestamp en milisegundos (string)
        
    Returns:
        str: Tiempo transcurrido en formato legible
    """
    try:
        # Convertir timestamp de milisegundos a segundos
        timestamp_seconds = int(timestamp) / 1000
        
        # Crear datetime object
        update_time = datetime.fromtimestamp(timestamp_seconds, tz=timezone.utc)
        current_time = datetime.now(timezone.utc)
        
        # Calcular diferencia
        time_diff = current_time - update_time
        
        # Formatear el tiempo transcurrido
        days = time_diff.days
        hours, remainder = divmod(time_diff.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        
        if days > 0:
            return f"hace {days}d {hours}h"
        elif hours > 0:
            return f"hace {hours}h {minutes}m"
        elif minutes > 0:
            return f"hace {minutes}m"
        else:
            return "hace unos segundos"
            
    except (ValueError, TypeError):
        return "Desconocido"


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
        md += "| ID | Título | Responsable | Estado | Estimación | Tiempo gastado | Última actualización | Último comentario |\n"
        md += "|-----|--------|------------|---------|------------|----------------|---------------------|-------------------|\n"


        for task in issues:
            assignee_name = task.assignee or "Sin asignar"
            estimation = task.estimation or "Sin est."
            spent = task.spent or "Sin tiempo"
            state = task.state or "Sin estado"
            time_elapsed = _calculate_time_elapsed(task.updated) if task.updated else "Desconocido"
            last_comment = task.last_comment or "Sin comentarios"

            md += f"| {task.id} | {task.summary} | {assignee_name} | {state} | {estimation} | {spent} | {time_elapsed} | {last_comment} |\n"

        return md