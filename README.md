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

## Configuración

### Variables de entorno requeridas

```bash
export YOUTRACK_BASE_URL="https://tu-instancia.youtrack.cloud"
export YOUTRACK_API_TOKEN="tu-token-de-api"
```

### Instalación

```bash
pip install -r requirements.txt
```

## Uso

### Como servidor MCP

```bash
python3 main.py
```

### Herramientas disponibles

#### `getTasksInformation(name: str) -> str`

Obtiene información de todas las tareas en progreso de un tablero específico.

**Parámetros:**
- `name`: Nombre del tablero de YouTrack

**Retorna:**
- Reporte en formato markdown con las tareas en progreso

**Ejemplo:**
```python
# Obtener tareas del tablero "Mi Proyecto"
resultado = getTasksInformation("Mi Proyecto")
```

## Características

- ✅ Manejo robusto de errores de API
- ✅ Validación de configuración
- ✅ Logging estructurado
- ✅ Separación de responsabilidades
- ✅ Modelos de datos tipados
- ✅ Filtrado de tareas terminadas vs en progreso