# Arquitectura y Responsabilidades de las Clases

## Descripción general
El proyecto Youtrack-MCP sigue una arquitectura modular con separación clara de responsabilidades, donde cada módulo y clase tiene un propósito específico y bien definido.

## Módulos y sus Funcionalidades

### 📁 `main.py`
**Propósito**: Punto de entrada y gestión de argumentos del servidor MCP

**Funcionalidades**:
- **Gestión de argumentos de línea de comandos**:
  - `--timeout`: Timeout para requests HTTP (default: 30 segundos)
  - `--finished-states`: Estados considerados terminados (default: "Fixed,Verified")
- **Inicialización del servidor**: Configura y ejecuta el servidor MCP con los parámetros proporcionados
- **Interfaz de usuario**: Proporciona help y validación básica de argumentos

**Elementos principales**:
- `main()`: Función principal que parsea argumentos y ejecuta `run_server()`

---

### 📁 `server.py`
**Propósito**: Clase de más alto nivel que declara las herramientas MCP y coordina el resto de clases

**Funcionalidades**:
- **Declaración de herramientas MCP**: Define las herramientas que el servidor expone (`getTasksInformation`, `getIssueById`)
- **Coordinación de componentes**: Utiliza y coordina `config`, `client`, `formatter` para ejecutar las operaciones
- **Validación de alto nivel**: Valida configuración y parámetros antes de delegar a otros componentes
- **Manejo de errores globales**: Captura errores de todos los componentes y los presenta de forma user-friendly
- **Logging de operaciones**: Registra actividad de las herramientas para debugging

**Elementos principales**:
- `getTasksInformation(name, num_comments)`: Herramienta para obtener reporte de tablero
- `getIssueById(issue_id)`: Herramienta para análisis detallado de issue específica
- `run_server()`: Función que inicializa y ejecuta el servidor MCP
- Instancias globales: `config`, `client`, `formatter` para coordinación

---

### 📁 `config.py`
**Propósito**: Gestión centralizada de configuración para comunicación con YouTrack

**Funcionalidades**:
- **Gestión de variables de entorno**: Lee y valida `YOUTRACK_BASE_URL` y `YOUTRACK_API_TOKEN`
- **Configuración de parámetros**: Gestiona timeout y finished_states que se establecen al inicio
- **Validación de configuración**: Verifica que todos los parámetros requeridos estén presentes
- **Headers HTTP**: Genera headers de autenticación para API calls
- **Inmutabilidad**: Los valores se fijan al inicio y permanecen constantes durante toda la ejecución

**Elementos principales**:
- `YouTrackConfig`: Clase que encapsula toda la configuración
  - `base_url`: URL de la API de YouTrack
  - `api_token`: Token de autenticación
  - `timeout`: Timeout para requests HTTP
  - `finished_states`: Lista de estados considerados terminados
  - `headers`: Property que genera headers HTTP con autenticación
  - `is_configured`: Property que valida si la configuración está completa

---

### 📁 `models.py`
**Propósito**: Modelos de datos para elementos de YouTrack con funcionalidades adicionales

**Funcionalidades**:
- **Definición de estructuras de datos**: Define atributos y tipos para Board, Issue, ExtendedIssue
- **Transformación JSON → Objeto**: Extrae y transforma datos del JSON de YouTrack API
- **Funcionalidades adicionales**: Métodos utilitarios para trabajar con los datos
- **Validación de datos**: Type hints y validación de campos
- **Abstracción de API**: Oculta la complejidad de la estructura JSON de YouTrack

**Elementos principales**:

#### `Board`
- **Atributos**: `id`, `name`, `current_sprint_id`, `current_sprint_name`
- **Propósito**: Representa un tablero ágil de YouTrack

#### `Issue`
- **Atributos**: `id`, `idReadable`, `summary`, `state`, `assignee`, `estimation`, `spent`, `updated`, `comments`
- **Métodos**:
  - `get_api_fields()`: Define qué campos solicitar a la API
  - `from_youtrack_data()`: Convierte JSON de YouTrack a objeto Issue
  - `is_finished()`: Determina si una issue está terminada
- **Funcionalidades especiales**: Manejo de comentarios múltiples, cálculo de tiempo transcurrido

#### `ExtendedIssue`
- **Hereda de Issue**: Extiende funcionalidad para análisis detallado
- **Campos adicionales**: `description` para análisis completo
- **Propósito**: Versión extendida para la herramienta `getIssueById`

---

### 📁 `youtrack_client.py`
**Propósito**: Manejo de llamadas HTTP a la API de YouTrack

**Funcionalidades**:
- **Gestión de requests HTTP**: Realiza todas las llamadas a YouTrack API
- **Manejo específico de errores**: Traduce errores HTTP a mensajes user-friendly
- **Uso de modelos**: Utiliza los modelos para determinar qué campos solicitar y crear objetos
- **Abstracción de API**: Oculta complejidad de endpoints y parámetros de YouTrack
- **Retry logic**: Manejo robusto de timeouts y errores de red

**Elementos principales**:
- `YouTrackAPIError`: Excepción personalizada para errores de API
- `YouTrackClient`: Cliente principal con métodos:
  - `get_boards()`: Obtiene lista de tableros disponibles
  - `get_sprint_issues(board_name, num_comments)`: Obtiene issues de un tablero específico
  - `find_board_by_name(name)`: Busca tablero por nombre
  - `get_issue_by_id(issue_id)`: Obtiene issue específica por ID
- **Uso de modelos**: Llama a `Issue.get_api_fields()` y `Issue.from_youtrack_data()`

---

### 📁 `utils.py`
**Propósito**: Cajón de sastre para funciones compartidas, evitando dependencias circulares

**Funcionalidades**:
- **Funciones utilitarias**: Operaciones comunes que varios módulos necesitan
- **Evitar dependencias circulares**: Centraliza funciones que de otra forma crearían imports cruzados
- **Reutilización de código**: Funciones que se usan en múltiples contextos

**Elementos principales**:
- `_calculate_time_elapsed(timestamp)`: Calcula tiempo transcurrido desde timestamp
  - Usado por models.py para formatear fechas
  - Usado por formatters.py para reportes
  - Evita duplicación de lógica de cálculo temporal

---

### 📁 `formatters.py`
**Propósito**: Generación de salida en markdown optimizada para IA

**Funcionalidades**:
- **Formateo de reportes**: Convierte datos de modelos a markdown estructurado
- **Optimización para IA**: Formato diseñado para ser procesado fácilmente por sistemas de IA
- **Presentación de datos**: Tablas, secciones y formato legible para humanos
- **Análisis y recomendaciones**: Genera insights automáticos sobre los datos

**Elementos principales**:
- `MarkdownFormatter`: Clase principal de formateo
  - `format_tasks_report(board, issues)`: Genera reporte completo de tablero
  - `format_extended_issue(issue)`: Genera análisis detallado de issue específica

## Flujo de interacción entre componentes

1. **`main.py`** → Lee argumentos y ejecuta **`server.py`**
2. **`server.py`** → Inicializa **`config.py`**, **`youtrack_client.py`**, **`formatters.py`**
3. **Herramientas MCP** → Validan parámetros y delegan a **`youtrack_client.py`**
4. **`youtrack_client.py`** → Usa **`models.py`** para determinar campos y crear objetos
5. **`models.py`** → Usa **`utils.py`** para operaciones de transformación
6. **`formatters.py`** → Usa **`utils.py`** para formateo y presenta resultado final

Esta arquitectura garantiza:
- **Separación de responsabilidades**: Cada clase tiene un propósito específico
- **Reutilización**: Componentes pueden ser usados independientemente
- **Mantenibilidad**: Cambios en un área no afectan otras
- **Testabilidad**: Cada componente puede ser probado de forma aislada