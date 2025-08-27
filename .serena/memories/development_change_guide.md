# Guía Rápida para Hacer Cambios

## 🎯 Dónde hacer cada tipo de cambio

### 📁 `main.py`
**Cuándo modificar**: Solo para añadir argumentos al servidor MCP
- ✅ Nuevos argumentos de línea de comandos (ej: `--debug`, `--cache-timeout`)
- ✅ Cambiar valores por defecto de argumentos existentes
- ❌ NO añadir lógica de negocio aquí

**Ejemplo**:
```python
parser.add_argument(
    "--debug", 
    action="store_true",
    help="Activar modo debug"
)
```

---

### 📁 `server.py`
**Cuándo modificar**: Para añadir nuevas herramientas MCP
- ✅ Nuevas herramientas MCP (funciones con `@mcp.tool()`)
- ✅ Modificar herramientas existentes
- ✅ Cambiar validaciones globales
- ❌ NO añadir lógica específica de YouTrack API

**Ejemplo**:
```python
@mcp.tool()
def getProjectStatistics(project_id: str) -> str:
    """Nueva herramienta para estadísticas de proyecto"""
    # Validaciones
    # Delegación a client
    # Formateo con formatter
```

---

### 📁 `config.py`
**Cuándo modificar**: Para nuevas configuraciones del servidor
- ✅ Nuevas variables de entorno
- ✅ Nuevos parámetros de configuración
- ✅ Cambiar validaciones de configuración
- ❌ NO añadir lógica de API calls

**Ejemplo**:
```python
self.debug_mode: bool = os.getenv('YOUTRACK_DEBUG', 'false').lower() == 'true'
self.cache_timeout: int = cache_timeout or 300
```

---

### 📁 `models.py`
**Cuándo modificar**: Para nuevos datos de YouTrack o campos adicionales
- ✅ Nuevos modelos (ej: `Project`, `User`, `Comment`)
- ✅ Nuevos campos en modelos existentes
- ✅ Nuevos métodos utilitarios en modelos
- ✅ Cambiar transformación JSON → Objeto

**Ejemplo**:
```python
@dataclass
class Project:
    id: str
    name: str
    description: Optional[str]
    
    @classmethod
    def from_youtrack_data(cls, data: dict) -> 'Project':
        # Lógica de transformación
```

---

### 📁 `youtrack_client.py`
**Cuándo modificar**: Para nuevas llamadas a YouTrack API
- ✅ Nuevos endpoints de YouTrack
- ✅ Modificar parámetros de llamadas existentes
- ✅ Nuevo manejo de errores específicos
- ❌ NO añadir formateo de salida aquí

**Ejemplo**:
```python
def get_project_details(self, project_id: str) -> Tuple[Optional[Project], Optional[str]]:
    """Obtiene detalles de un proyecto específico"""
    # Lógica de API call
    # Creación de objeto Project
    # Manejo de errores
```

---

### 📁 `formatters.py`
**Cuándo modificar**: Para cambiar formato de salida
- ✅ Nuevos formatos de reporte
- ✅ Modificar estructura de markdown existente
- ✅ Nuevos tipos de análisis automático
- ❌ NO añadir lógica de API o transformación de datos

**Ejemplo**:
```python
def format_project_report(self, project: Project, issues: List[Issue]) -> str:
    """Genera reporte detallado de proyecto"""
    # Formateo en markdown
    # Análisis automático
    # Recomendaciones
```

---

### 📁 `utils.py`
**Cuándo modificar**: Para funciones compartidas entre módulos
- ✅ Nuevas funciones utilitarias
- ✅ Funciones que se usan en 2+ módulos
- ✅ Operaciones de formateo/cálculo comunes
- ✅ Evitar dependencias circulares

**Ejemplo**:
```python
def format_duration(minutes: int) -> str:
    """Convierte minutos a formato legible (ej: 2h 30m)"""
    # Lógica de formateo compartida
```

---

## 🔄 Flujo típico para nuevas funcionalidades

### Para añadir nueva herramienta MCP:
1. **`models.py`** → Crear/modificar modelo si es necesario
2. **`youtrack_client.py`** → Añadir método para API call
3. **`formatters.py`** → Crear método de formateo
4. **`server.py`** → Crear herramienta MCP que coordine todo
5. **`utils.py`** → Añadir funciones compartidas si es necesario

### Para nueva configuración:
1. **`config.py`** → Añadir nueva configuración
2. **`main.py`** → Añadir argumento si es necesario
3. **Módulos que lo usen** → Acceder via `config.nuevo_parametro`

### Para nuevo endpoint de YouTrack:
1. **`models.py`** → Crear modelo si es necesario
2. **`youtrack_client.py`** → Implementar llamada API
3. **`formatters.py`** → Crear formateo si es necesario
4. **`server.py`** → Usar en herramienta MCP

---

## ⚠️ Reglas importantes

- **Un archivo, una responsabilidad**: No mezclar concerns
- **server.py coordina**: No implementar lógica específica ahí
- **models.py define estructura**: Solo transformación de datos
- **client.py maneja API**: Solo llamadas HTTP y errores
- **formatters.py presenta**: Solo formato de salida
- **utils.py comparte**: Solo funciones reutilizables
- **config.py configura**: Solo parámetros y validación

---

## 🧪 Después de cambios

1. **Actualizar tests** si existen
2. **Verificar con Inspector MCP** que funciona
3. **Actualizar README.md** si añades herramientas
4. **Escribir memoria** si es cambio significativo