"""
Formateadores para generar salidas en diferentes formatos
"""
from typing import List, Dict, Any
from .models import Issue


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
        md += "| ID | Título | Responsable | Estado | Estimación | Tiempo gastado | ⚠️ Alertas |\n"
        md += "|-----|--------|------------|---------|------------|----------------|------------|\n"
        
        # Contadores para estadísticas
        total_tasks = len(issues)
        issues_with_problems = []
        
        for task in issues:
            assignee_name = task.assignee or "Sin asignar"
            estimation = task.estimation or "Sin est."
            spent = task.spent or "Sin tiempo"
            state = task.state or "Sin estado"
            
            # Generar alertas para esta tarea
            alerts = MarkdownFormatter._generate_task_alerts(task)
            alerts_text = ", ".join(alerts) if alerts else "✅"
            
            if alerts:
                issues_with_problems.append(task)
            
            md += f"| {task.id} | {task.summary} | {assignee_name} | {state} | {estimation} | {spent} | {alerts_text} |\n"
        
        # Añadir tabla de resumen de problemas
        md += MarkdownFormatter._generate_problems_summary(issues_with_problems, total_tasks)
        
        return md
    
    @staticmethod
    def _generate_task_alerts(task: Issue) -> List[str]:
        """
        Genera alertas específicas para una tarea
        
        Args:
            task: Issue a analizar
            
        Returns:
            List[str]: Lista de alertas encontradas
        """
        alerts = []
        
        # Verificar si no tiene asignado
        if not task.assignee:
            alerts.append("🔴 Sin asignar")
        
        # Verificar si no tiene estimación
        if not task.estimation:
            alerts.append("🟡 Sin estimación")
        
        # Verificar si el tiempo gastado supera la estimación
        if task.estimation and task.spent:
            estimated_time = MarkdownFormatter._parse_time(task.estimation)
            spent_time = MarkdownFormatter._parse_time(task.spent)
            
            if estimated_time > 0 and spent_time > estimated_time:
                alerts.append("🟠 Tiempo excedido")
        
        return alerts
    
    @staticmethod
    def _parse_time(time_str: str) -> float:
        """
        Convierte string de tiempo a horas (aproximado)
        
        Args:
            time_str: String de tiempo (ej: "2h 30m", "1d", "30m")
            
        Returns:
            float: Tiempo en horas
        """
        if not time_str:
            return 0.0
        
        # Convertir a minusculas para parsing
        time_str = time_str.lower().strip()
        
        total_hours = 0.0
        
        # Buscar días (d)
        if 'd' in time_str:
            try:
                days_part = time_str.split('d')[0].strip()
                days = float(days_part)
                total_hours += days * 8  # Asumimos 8 horas por día
                # Quitar la parte de días para procesar el resto
                time_str = time_str.split('d')[1].strip() if 'd' in time_str else time_str
            except:
                pass
        
        # Buscar horas (h)
        if 'h' in time_str:
            try:
                # Extraer la parte antes de 'h'
                h_part = time_str.split('h')[0].strip()
                hours = float(h_part)
                total_hours += hours
                # Quitar la parte de horas para procesar minutos
                time_str = time_str.split('h')[1].strip() if 'h' in time_str else ""
            except:
                pass
        
        # Buscar minutos (m) - ahora también procesa si hay horas
        if 'm' in time_str:
            try:
                # Extraer la parte antes de 'm'
                m_part = time_str.split('m')[0].strip()
                if m_part:  # Solo si hay algo antes de 'm'
                    minutes = float(m_part)
                    total_hours += minutes / 60
            except:
                pass
        
        return total_hours
    
    @staticmethod
    def _generate_problems_summary(problem_issues: List[Issue], total_tasks: int) -> str:
        """
        Genera un resumen de problemas encontrados
        
        Args:
            problem_issues: Lista de issues con problemas
            total_tasks: Total de tareas analizadas
            
        Returns:
            str: Sección de resumen en markdown
        """
        if not problem_issues:
            return "\n## ✅ Resumen\n\n**¡Excelente!** Todas las tareas están bien configuradas.\n"
        
        md = f"\n## ⚠️ Resumen de Problemas\n\n"
        md += f"**{len(problem_issues)} de {total_tasks} tareas** tienen problemas que requieren atención:\n\n"
        
        # Contar tipos de problemas
        unassigned = sum(1 for issue in problem_issues if not issue.assignee)
        no_estimation = sum(1 for issue in problem_issues if not issue.estimation)
        time_exceeded = sum(1 for issue in problem_issues 
                          if issue.estimation and issue.spent and 
                          MarkdownFormatter._parse_time(issue.spent) > MarkdownFormatter._parse_time(issue.estimation))
        
        if unassigned > 0:
            md += f"- 🔴 **{unassigned} tareas sin asignar**\n"
        if no_estimation > 0:
            md += f"- 🟡 **{no_estimation} tareas sin estimación**\n"
        if time_exceeded > 0:
            md += f"- 🟠 **{time_exceeded} tareas con tiempo excedido**\n"
        
        return md
