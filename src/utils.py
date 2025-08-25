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
