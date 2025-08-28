# Youtrack-mcp

Servidor MCP (Model Context Protocol) para integración con YouTrack que permite obtener información de tableros ágiles y generar reportes detallados de tareas en progreso.

## Descripción

Este servidor MCP proporciona herramientas avanzadas para:
- Conectarse a la API de YouTrack con manejo robusto de errores
- Obtener información completa de tableros ágiles
- Generar reportes en markdown de tareas en progreso con análisis de problemas
- Obtener información detallada de issues específicas con todos sus comentarios

## Arquitectura y Estructura del proyecto

El proyecto sigue una arquitectura modular con separación clara de responsabilidades:

```
youtrack-mcp/
├── src/
│   ├── __init__.py
│   ├── main.py          # Punto de entrada principal del servidor MCP
│   ├── config.py        # Gestión de configuración y variables de entorno
│   ├── models.py        # Modelos de datos tipados (Board, Issue) con validación
│   ├── youtrack_client.py  # Cliente HTTP para la API de YouTrack con manejo de errores
│   ├── formatters.py    # Formateadores de salida en markdown optimizados para IA
│   └── server.py        # Implementación del servidor MCP con herramientas disponibles
├── pyproject.toml       # Configuración del proyecto y dependencias (Python 3.12+)
├── uv.lock             # Lock file para reproducibilidad de dependencias
├── requirements.txt     # Dependencias tradicionales (compatibilidad)
└── README.md           # Documentación del proyecto
```

### Componentes principales

- **`config.py`**: Validación y gestión centralizada de variables de entorno
- **`models.py`**: Modelos de datos con type hints para Board e Issue, incluyendo manejo de comentarios múltiples
- **`youtrack_client.py`**: Cliente HTTP con retry logic y manejo específico de errores de API
- **`formatters.py`**: Generadores de markdown estructurado para análisis por IA
- **`server.py`**: Servidor MCP con herramientas `getTasksInformation` y `getIssueById`

### Flujo de datos

1. El cliente MCP invoca una herramienta del servidor
2. El servidor valida configuración y parámetros
3. Se realiza la consulta a YouTrack API a través del cliente HTTP
4. Los datos se procesan con los modelos tipados
5. Se genera el reporte en markdown usando los formateadores
6. Se retorna el resultado estructurado al cliente MCP

## Instalación y Desarrollo

### Requisitos

- Python 3.12 o superior
- `uv` (recomendado) o `pip` para gestión de dependencias
- Acceso a una instancia de YouTrack con permisos de API

### Instalación para desarrollo

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/Digio-Campus/Youtrack-mcp.git
   cd Youtrack-mcp
   ```

2. **Instalar dependencias con uv (recomendado):**
   ```bash
   # Instalar uv si no lo tienes
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Instalar dependencias del proyecto
   uv sync
   ```

3. **Configurar variables de entorno:**
   ```bash
   # Crear archivo .env (opcional)
   export YOUTRACK_BASE_URL="https://tu-instancia.youtrack.cloud/api"
   export YOUTRACK_API_TOKEN="tu-token-de-api"
   ```

4. **Ejecutar el servidor localmente:**
   ```bash
   # Con uv
   uv run youtrack-mcp
   
   # O directamente con Python
   YOUTRACK_BASE_URL="<url>" YOUTRACK_API_TOKEN="<token>" python3 src/main.py
   ```

### Instalación como dependencia

```bash
# Instalar desde GitHub
pip install git+https://github.com/Digio-Campus/Youtrack-mcp.git

# O usar uvx para ejecución directa
uvx --from git+https://github.com/Digio-Campus/Youtrack-mcp youtrack-mcp
```

## Uso

### Configuración en cliente MCP

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

#### `getTasksInformation(name: str, num_comments: int = 1) -> str`

Obtiene información completa de todas las tareas en progreso de un tablero específico.

**Parámetros:**
- `name`: Nombre del tablero de YouTrack
- `num_comments` (opcional): Número de comentarios recientes a incluir por tarea
  - `1` (default): Solo el último comentario
  - `> 1`: Los últimos N comentarios ordenados cronológicamente
  - `0`: Sin comentarios

**Retorna:**
Reporte en markdown que incluye:
- **Tabla de tareas en progreso** con:
  - ID de la issue
  - Título/resumen
  - Asignado a
  - Estado actual
  - Tiempo estimado vs tiempo gastado
  - Tiempo desde la última actualización
  - Comentarios recientes (según parámetro `num_comments`)

**Ejemplos de uso:**
```python
# Obtener reporte básico con último comentario
getTasksInformation("Sprint Actual")

# Incluir los últimos 3 comentarios por tarea
getTasksInformation("Sprint Actual", num_comments=3)

# Sin comentarios para vista rápida
getTasksInformation("Sprint Actual", num_comments=0)
```

#### `getIssueById(issue_id: str) -> str`

Obtiene información detallada y completa de una issue específica por su ID. Diseñada para análisis profundo de issues problemáticas identificadas previamente.

**Parámetros:**
- `issue_id`: ID de la issue a analizar. Acepta:
  - ID legible (ej: "DEMO-123", "PROJ-456")
  - ID interno (ej: "3-3", "2-15")

**Retorna:**
Información completa en markdown estructurado que incluye:
- **Metadatos de la issue**:
  - ID, título, estado, prioridad
  - Asignado, reportado por, fechas
  - Tiempo estimado vs gastado
- **Descripción completa** (si está disponible)
- **Historial completo de comentarios**:
  - Ordenados cronológicamente (más antiguo → más reciente)
  - Autor, contenido y timestamp de cada comentario

**Ejemplo de uso:**
```python
# Análisis detallado de issue específica
getIssueById("PROJ-123")

# También funciona con IDs internos
getIssueById("3-15")
```

## Testing y Desarrollo

### Testing con Inspector MCP

Para probar el servidor MCP de forma interactiva, utiliza el inspector oficial de Model Context Protocol:

```bash
# Ejecutar el inspector con las variables de entorno configuradas
YOUTRACK_API_TOKEN="tu-token-aqui" \
YOUTRACK_BASE_URL="https://tu-instancia.youtrack.cloud/api" \
npx @modelcontextprotocol/inspector uv --directory . run youtrack-mcp
```

Esto iniciará:
- **Servidor proxy** en puerto 6277
- **Interfaz web** en puerto 6274 para testing interactivo
- **Debugging** de mensajes entre cliente y servidor MCP

### Requisitos para testing

- **Node.js y npm** instalados
- **uv** para gestión de dependencias Python
- **Variables de entorno** configuradas correctamente

### Ejecución directa para debugging

```bash
# Ejecución básica
env YOUTRACK_BASE_URL="<url>" YOUTRACK_API_TOKEN="<token>" python3 src/main.py

# Con argumentos opcionales
env YOUTRACK_BASE_URL="<url>" YOUTRACK_API_TOKEN="<token>" \
python3 src/main.py --timeout 30 --finished-states "Done,Closed"
```

## Ejemplos prácticos

### Caso de uso 1: Monitoreo de Sprint

```python
# Obtener vista completa del sprint actual con comentarios recientes
response = getTasksInformation("Sprint 2024-08", num_comments=2)
```

**Salida esperada:**
```markdown
# Reporte de Tareas - Sprint 2024-08

## 📊 Resumen del tablero
- **Total de tareas en progreso:** 8
- **Tareas sin asignar:** 1
- **Tiempo total estimado:** 45h
- **Tiempo total gastado:** 32h

## 📋 Tareas en progreso

| ID | Título | Asignado | Estado | Estimado | Gastado | Última actualización | Comentarios |
|---|---|---|---|---|---|---|---|
| DEMO-123 | Implementar API REST | Juan Pérez | In Progress | 8h | 6h | hace 2 días | Juan: Avanzando con endpoints<br>María: Revisar documentación |
| DEMO-124 | Diseño UI login | María García | Review | 4h | 5h | hace 1 día | María: Listo para revisión |

## ⚠️ Problemas detectados
- **Tarea DEMO-123**: Sin actualizaciones en 2 días
- **Sobrecarga de María García**: 3 tareas asignadas

## 💡 Recomendaciones
- Hacer seguimiento de DEMO-123 con Juan Pérez
- Considerar redistribuir carga de María García
```

### Caso de uso 2: Análisis de issue problemática

```python
# Investigar issue específica con historial completo
response = getIssueById("DEMO-125")
```

**Salida esperada:**
```markdown
# Issue Detallada: DEMO-125

## 📋 Información básica
| Campo | Valor |
|---|---|
| **ID** | DEMO-125 |
| **Título** | Bug crítico en autenticación |
| **Estado** | Open |
| **Prioridad** | Critical |
| **Asignado** | Juan Pérez |
| **Reportado por** | María García |

## 📝 Descripción
El sistema de autenticación falla intermitentemente causando logout automático...

## 💬 Historial de comentarios

### María García - hace 3 días
Detectado el bug en producción. Afecta al 15% de usuarios...

### Juan Pérez - hace 2 días  
Investigando logs del servidor. Parece relacionado con sesiones...

## 🔍 Resumen para análisis
- **Criticidad alta**: Bug en producción afectando usuarios
- **Investigación en curso**: Juan trabajando en logs
- **Siguiente paso**: Revisar gestión de sesiones
```

## Características principales

- ✅ **Manejo robusto de errores** de API con mensajes informativos
- ✅ **Validación completa** de configuración y parámetros
- ✅ **Logging estructurado** para debugging y monitoreo
- ✅ **Separación clara de responsabilidades** por módulos
- ✅ **Modelos de datos tipados** con validación automática
- ✅ **Filtrado inteligente** de tareas terminadas vs en progreso
- ✅ **Comentarios múltiples** con control granular
- ✅ **Optimizado para IA** con formatos estructurados
- ✅ **Testing integrado** con Inspector MCP

## Documentación del Proyecto

### Instrucciones para IA y Memorias del Proyecto

Este proyecto incluye documentación especializada para facilitar el desarrollo asistido por IA:

#### `.github/copilot-instructions.md`
Instrucciones específicas para GitHub Copilot que incluyen:
- **Descripción del proyecto** y objetivos principales
- **Integración con Serena MCP** como herramientas de desarrollo
- **Inicialización correcta** del proyecto con Serena
- **Gestión de memorias** para recordar decisiones y patrones de código
- **Herramientas de análisis** semántico de código
- **Guías de uso** de las herramientas de Serena para diferentes escenarios

#### `.serena/memories/`
Sistema de memorias del proyecto gestionado por Serena MCP:

- **`main_memory_index.md`** - 📌 Punto de entrada principal para navegar todas las memorias
- **`project_overview.md`** - 🌟 Overview general del proyecto, tech stack y herramientas
- **`architecture_class_responsibilities.md`** - 🏗️ Arquitectura detallada y responsabilidades de cada clase
- **`development_change_guide.md`** - 🔧 Guía práctica para realizar cambios en el código
- **`style_and_conventions.md`** - 🎨 Convenciones de código y patrones utilizados
- **`testing_procedures.md`** - 🧪 Procedimientos de testing con Inspector MCP

### Beneficios de la Documentación para IA

- **Onboarding rápido**: Cualquier IA puede entender el proyecto leyendo las memorias
- **Desarrollo consistente**: Las convenciones y patrones están documentados
- **Navegación eficiente**: Sistema de memorias interconectadas para acceso directo
- **Mantenimiento simplificado**: Decisiones arquitectónicas y de diseño preservadas
- **Colaboración mejorada**: Contexto compartido entre desarrolladores y herramientas de IA
