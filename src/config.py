"""
Configuración del servidor MCP YouTrack
"""
import os
import logging
from typing import Optional, List

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Youtrack MCP")

class YouTrackConfig:
    """Configuración para el cliente de YouTrack"""
    
    def __init__(self, timeout: int = 30, finished_states: Optional[List[str]] = None):
        """
        Inicializa la configuración de YouTrack
        
        Args:
            timeout: Timeout para requests HTTP en segundos (default: 30)
            finished_states: Lista de estados considerados como terminados 
                           (default: ["Fixed", "Verified"])
        """
        # Variables de entorno requeridas
        self.base_url: Optional[str] = os.getenv('YOUTRACK_BASE_URL')
        self.api_token: Optional[str] = os.getenv('YOUTRACK_API_TOKEN')
        
        # Parámetros configurables
        self.timeout = timeout
        self.finished_states = finished_states or ["Fixed", "Verified"]
        
        # Validar configuración
        self._validate_config()
        
        # Normalizar URL
        if self.base_url:
            self.base_url = self.base_url.rstrip('/')
    
    def _validate_config(self) -> None:
        """Valida que la configuración esté completa"""
        if not self.base_url:
            logger.error("Variable de entorno YOUTRACK_BASE_URL no configurada")
        if not self.api_token:
            logger.error("Variable de entorno YOUTRACK_API_TOKEN no configurada")
    
    @property
    def headers(self) -> dict:
        """Retorna los headers para las peticiones API"""
        if not self.api_token:
            return {}
        
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Accept": "application/json"
        }
    
    @property
    def is_configured(self) -> bool:
        """Verifica si la configuración está completa"""
        return bool(self.base_url and self.api_token)
