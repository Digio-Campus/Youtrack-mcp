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
├── main.py              # Punto de entrada principal
├── src/
│   ├── __init__.py
│   ├── config.py        # Configuración y variables de entorno
│   ├── models.py        # Modelos de datos (Board, Issue)
│   ├── youtrack_client.py  # Cliente para la API de YouTrack
│   ├── formatters.py    # Formateadores de salida (markdown)
│   └── server.py        # Servidor MCP
├── requirements.txt     # Dependencias
└── README.md           # Este archivo
```

## Uso

### Como servidor MCP

El servidor se ejecuta automáticamente cuando se configura en un cliente MCP compatible. La configuración se realiza a través del archivo `mcp.json` como se muestra abajo.

### Ejecución directa (desarrollo/testing)

```bash
# Con variables de entorno del sistema
export YOUTRACK_BASE_URL="https://tu-instancia.youtrack.cloud/api"
export YOUTRACK_API_TOKEN="tu-token"

# Ejecutar servidor
python3 main.py

# Con argumentos personalizados
python3 main.py --timeout 60 --finished-states "Done,Closed"
```

### Como servidor MCP

Este servidor se configura a través de un archivo `mcp.json` que especifica las variables de entorno y argumentos del servidor.

**Ejemplo de configuración en `mcp.json`:**

```json
{
    "servers": {
        "youtrack": {
            "type": "stdio",
            "command": "/path/to/python",
            "args": [
                "main.py",
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

### Instalación

```bash
pip install -r requirements.txt
```

### Herramientas disponibles

#### `getTasksInformation(name: str) -> str`

Obtiene información de todas las tareas en progreso de un tablero específico.

**Parámetros:**
- `name`: Nombre del tablero de YouTrack

**Retorna:**
- Reporte en formato markdown con las tareas en progreso

## Características

- ✅ Manejo robusto de errores de API
- ✅ Validación de configuración
- ✅ Logging estructurado
- ✅ Separación de responsabilidades
- ✅ Modelos de datos tipados
- ✅ Filtrado de tareas terminadas vs en progreso