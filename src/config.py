"""
Configuración del servidor MCP YouTrack
"""
import os
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Youtrack MCP")

class YouTrackConfig:
    """Configuración para el cliente de YouTrack"""
    
    def __init__(self):
        self.base_url: Optional[str] = os.getenv('YOUTRACK_BASE_URL')
        self.api_token: Optional[str] = os.getenv('YOUTRACK_API_TOKEN')
        
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
