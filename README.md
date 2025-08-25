# Youtrack-mcp

Servidor MCP (Model Context Protocol) para integración con YouTrack que permite obtener información de tableros ágiles y generar reportes de tareas en progreso.

## Descripción

Este servidor MCP proporciona herramientas para:
- Conectarse a la API de YouTrack
- Obtener información de tableros ágiles
- Generar reportes en markdown de tareas en progreso

## Estructura del proyecto

```
youtrack-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py          # Punto de entrada principal  
│   ├── config.py        # Configuración y variables de entorno
│   ├── models.py        # Modelos de datos (Board, Issue)
│   ├── youtrack_client.py  # Cliente para la API de YouTrack
│   ├── formatters.py    # Formateadores de salida (markdown)
│   └── server.py        # Servidor MCP
├── pyproject.toml       # Configuración del proyecto y dependencias
├── uv.lock             # Versiones exactas de dependencias
├── requirements.txt     # Dependencias (para compatibilidad)
└── README.md           # Este archivo
```

## Uso

El servidor se ejecuta automáticamente cuando se configura en un cliente MCP compatible.

La configuración, para VSCode, se realiza a través del archivo `mcp.json` que especifica las variables de entorno y argumentos del servidor.

**Ejemplo de configuración en `mcp.json`:**

```json
{
    "servers": {
        "youtrack": {
            "type": "stdio",
            "command": "uvx",
            "args": [
                "--from",
                "git+https://github.com/Digio-Campus/Youtrack-mcp",
                "youtrack-mcp",
                "--timeout",
                "30",
                "--finished-states",
                "Fixed,Verified"
            ],
            "env": {
                "YOUTRACK_API_TOKEN": "tu-token-de-api",
                "YOUTRACK_BASE_URL": "https://tu-instancia.youtrack.cloud/api"
            }
        }
    },
    "inputs": []
}
```

### Variables de entorno requeridas

- `YOUTRACK_BASE_URL`: URL de tu instancia de YouTrack (ej: `https://tu-instancia.youtrack.cloud/api`)
- `YOUTRACK_API_TOKEN`: Token de API de YouTrack

### Argumentos opcionales del servidor

- `--timeout`: Timeout para requests HTTP en segundos (default: 30)
- `--finished-states`: Estados considerados terminados, separados por comas (default: "Fixed,Verified")

### Herramientas disponibles

#### `getTasksInformation(name: str) -> str`

Obtiene información de todas las tareas en progreso de un tablero específico y genera un reporte completo con análisis de problemas.

**Parámetros:**
- `name`: Nombre del tablero de YouTrack

**Retorna:**
- Tabla con todas las tareas en progreso indicando:
    - id
    - nombre
    - responsable
    - estado
    - tiempo estimado
    - tiempo gastado
    - tiempo desde la ultima actualización
    - ultimo comentario

## Características

- ✅ Manejo robusto de errores de API
- ✅ Validación de configuración
- ✅ Logging estructurado
- ✅ Separación de responsabilidades
- ✅ Modelos de datos tipados
- ✅ Filtrado de tareas terminadas vs en progreso
