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
        
        # Información básica del modelo
        md += "## Información Básica\n\n"
        md += "| Campo | Valor |\n"
        md += "|-------|-------|\n"
        md += f"| **ID** | {issue.id} |\n"
        md += f"| **Título** | {issue.summary} |\n"
        md += f"| **Estado** | {issue.state or 'Sin estado'} |\n"
        md += f"| **Asignado a** | {issue.assignee or 'Sin asignar'} |\n"
        md += f"| **Estimación** | {issue.estimation or 'Sin estimación'} |\n"
        md += f"| **Tiempo gastado** | {issue.spent or 'Sin tiempo registrado'} |\n"
        
        if issue.updated:
            updated_elapsed = _calculate_time_elapsed(issue.updated)
            md += f"| **Última actualización** | {updated_elapsed} |\n"
        
        md += "\n"
        
        # Comentarios
        if issue.comments and len(issue.comments) > 0:
            md += f"## Comentarios ({len(issue.comments)} total)\n\n"
            chronological_comments = list(reversed(issue.comments))
            for i, comment in enumerate(chronological_comments, 1):
                md += f"### Comentario {i}\n"
                md += f"{comment}\n\n"
        else:
            md += "## Comentarios\n\n"
            md += "No hay comentarios disponibles.\n\n"
        
        # Datos completos del raw_data
        if issue.raw_data:
            md += MarkdownFormatter._format_raw_data_section(issue.raw_data)
        
        return md

    @staticmethod
    def _format_raw_data_section(raw_data: dict) -> str:
        """
        Formatea recursivamente todos los datos del raw_data de forma genérica
        
        Args:
            raw_data: Diccionario con todos los datos de la API
            
        Returns:
            str: Sección markdown con todos los datos
        """
        md = "## Datos Completos de la API\n\n"
        
        # Recorrer todos los campos del raw_data
        for field_name, field_value in raw_data.items():
            if field_name.startswith('$'):
                continue  # Saltar metadatos de la API
                
            md += f"### {field_name.replace('_', ' ').title()}\n\n"
            md += MarkdownFormatter._format_field_value(field_value)
            md += "\n"
        
        return md
    
    @staticmethod
    def _format_field_value(value, indent_level: int = 0) -> str:
        """
        Formatea cualquier tipo de valor de forma recursiva
        
        Args:
            value: Valor a formatear
            indent_level: Nivel de indentación para estructuras anidadas
            
        Returns:
            str: Valor formateado en markdown
        """
        indent = "  " * indent_level
        
        if value is None:
            return f"{indent}- Sin valor\n"
        elif isinstance(value, dict):
            if not value:
                return f"{indent}- Objeto vacío\n"
            
            result = ""
            for key, val in value.items():
                if key.startswith('$'):
                    continue
                clean_key = key.replace('_', ' ').title()
                result += f"{indent}- **{clean_key}**:\n"
                result += MarkdownFormatter._format_field_value(val, indent_level + 1)
            return result
        elif isinstance(value, list):
            if not value:
                return f"{indent}- Lista vacía\n"
            
            result = ""
            for i, item in enumerate(value):
                result += f"{indent}- **Item {i+1}**:\n"
                result += MarkdownFormatter._format_field_value(item, indent_level + 1)
            return result
        else:
            # Valor primitivo (str, int, float, bool)
            return f"{indent}- {str(value)}\n"
