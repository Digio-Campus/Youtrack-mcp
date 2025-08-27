# Estilo y convenciones de código

## Lenguaje y versión
- **Python 3.12+** con uso extensivo de features modernas
- **Type hints obligatorios** en todas las funciones, métodos y variables de clase
- **Dataclasses** para modelos de datos en lugar de clases tradicionales

## Estructura de archivos
- **Docstrings de módulo** al inicio de cada archivo explicando su propósito
- **Imports organizados**: stdlib → third-party → local imports
- **Logging configurado** con logger específico `"Youtrack MCP"` en cada módulo

## Convenciones de nomenclatura
- **Clases**: PascalCase (ej: `YouTrackConfig`, `MarkdownFormatter`)
- **Funciones y variables**: snake_case (ej: `get_boards`, `base_url`)
- **Constantes**: UPPER_SNAKE_CASE (ej: variables de entorno)
- **Métodos privados**: prefijo `_` (ej: `_calculate_time_elapsed`, `_validate_config`)

## Documentación
- **Docstrings detallados** en todas las funciones y clases públicas
- **Formato Google/NumPy style** con secciones Args, Returns, Raises cuando aplique
- **Comentarios explicativos** en lógica compleja, especialmente transformaciones de datos
- **Type hints como documentación** - son parte integral del código

## Manejo de errores
- **Validación explícita** en puntos de entrada (argumentos, configuración)
- **Logging estructurado** con levels apropiados (INFO para operaciones, ERROR para fallos)
- **Excepciones específicas** (ej: `YouTrackAPIError`) en lugar de genéricas
- **Tuple returns** para operaciones que pueden fallar: `(result, error)`
- **Manejo granular** de diferentes tipos de errores HTTP (404, 403, etc.)

## Arquitectura de datos
- **Dataclasses con defaults** para modelos inmutables
- **Optional types** para campos que pueden no existir
- **Separación de concerns**: modelos básicos vs extendidos (`Issue` vs `ExtendedIssue`)
- **Raw data preservation** - mantener datos completos para análisis posterior

## Patrones de código
- **Factory methods** en modelos (ej: `from_youtrack_data()`)
- **Configuration objects** en lugar de variables globales dispersas
- **Dependency injection** - pasar configuración explícitamente
- **Single responsibility** - cada función tiene un propósito claro y específico

## Formatos y estructura
- **Indentación**: 4 espacios (estándar Python)
- **Líneas largas**: división lógica preservando legibilidad
- **F-strings** para interpolación de strings
- **Comprehensions** para transformaciones simples de datos

## Variables globales
- **Minimizar uso** - solo para instancias de coordinación (config, client, formatter)
- **Inicialización controlada** en función específica (`run_server()`)
- **Scope bien definido** - evitar side effects inesperados

## Logging y debugging
- **Logger específico** del proyecto: `"Youtrack MCP"`
- **Mensajes informativos** para operaciones exitosas
- **Context en logs** - incluir IDs, nombres de tableros, cantidades de datos
- **No logging de datos sensibles** (tokens, URLs privadas)

## Herramientas recomendadas
- **uv** para gestión de dependencias (moderno y rápido)
- **Type checking** con herramientas como mypy (aunque no configurado actualmente)
- **Black/isort** para formateo automático (recomendado para futuro)
- **Testing** con Inspector MCP para validación funcional

## Principios de diseño aplicados
- **Explicit is better than implicit** - configuración y dependencias claras
- **Fail early** - validación temprana de configuración y parámetros
- **Separation of concerns** - cada módulo tiene responsabilidad específica
- **Progressive enhancement** - modelos básicos extensibles a detallados
- **API-first design** - estructura pensada para consumo por IA/herramientas