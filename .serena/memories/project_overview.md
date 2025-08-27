# Youtrack-MCP: Servidor MCP para YouTrack

## Propósito del proyecto
Servidor MCP (Model Context Protocol) en Python para integrarse con la API de YouTrack, permitiendo obtener información de tableros ágiles y generar reportes detallados de tareas en progreso, con análisis automatizado de problemas y recomendaciones para gestión de proyectos.

## Tech stack
- **Python 3.12+** (con type hints y dataclasses)
- **requests** - Cliente HTTP para YouTrack API
- **mcp** - Model Context Protocol framework
- **uv** - Gestión moderna de dependencias (recomendado)

## Herramientas MCP disponibles

### `getTasksInformation(name: str, num_comments: int = 1)`
- Obtiene reporte completo de tablero ágil
- Análisis automatizado de problemas (tareas estancadas, sobrecarga, etc.)
- Recomendaciones de gestión
- Control granular de comentarios (0, 1, o múltiples)

### `getIssueById(issue_id: str)`  
- Análisis detallado de issue específica
- Información completa: descripción, comentarios, metadatos
- Formato optimizado para análisis por IA
- Soporte de IDs legibles e internos

## Estructura modular del código
- **`main.py`** - Punto de entrada y gestión de argumentos
- **`src/server.py`** - Servidor MCP con herramientas disponibles
- **`src/config.py`** - Configuración centralizada (variables de entorno, validación)
- **`src/models.py`** - Modelos de datos tipados (Board, Issue, ExtendedIssue)
- **`src/youtrack_client.py`** - Cliente HTTP para YouTrack API
- **`src/formatters.py`** - Generadores de markdown estructurado
- **`src/utils.py`** - Funciones compartidas (cálculos de tiempo, etc.)

## Características principales
- **Arquitectura modular** con separación clara de responsabilidades
- **Manejo robusto de errores** con mensajes informativos
- **Optimizado para IA** con formatos estructurados
- **Testing integrado** con Inspector MCP
- **Configuración flexible** vía variables de entorno y argumentos
- **Logging estructurado** para debugging y monitoreo
- **Validación completa** de configuración y parámetros

## Configuración requerida

### Variables de entorno
- `YOUTRACK_BASE_URL` - URL de tu instancia YouTrack (ej: `https://tu-instancia.youtrack.cloud/api`)
- `YOUTRACK_API_TOKEN` - Token de API de YouTrack

### Argumentos opcionales
- `--timeout` - Timeout para requests HTTP (default: 30)
- `--finished-states` - Estados considerados terminados (default: "Fixed,Verified")

## Instalación y uso

### Desarrollo local
```bash
# Con uv (recomendado)
uv sync
uv run youtrack-mcp

# Con pip tradicional  
pip install -r requirements.txt
python3 src/main.py
```

### Como servidor MCP
Configurable vía `mcp.json` para integración con clientes MCP compatibles (VSCode, Claude Desktop, etc.)

### Testing
Usar Inspector MCP para pruebas interactivas:
```bash
YOUTRACK_API_TOKEN="<token>" YOUTRACK_BASE_URL="<url>" npx @modelcontextprotocol/inspector uv --directory . run youtrack-mcp
```

## Casos de uso típicos
- **Monitoreo de sprints** con detección automática de problemas
- **Análisis de issues críticas** con contexto completo 
- **Reportes ejecutivos** sin comentarios para vista rápida
- **Gestión de carga de trabajo** con recomendaciones automáticas
- **Integración con herramientas de IA** para análisis de proyectos