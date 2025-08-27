# Procedimientos de Pruebas para Youtrack-MCP

## Pruebas del Servidor MCP

### Inspector MCP
Para probar el servidor MCP de forma interactiva, usar el inspector oficial de Model Context Protocol:

```bash
# Ejecutar el inspector con las variables de entorno del proyecto
YOUTRACK_API_TOKEN="tu-token-de-api" YOUTRACK_BASE_URL="https://tu-instancia.youtrack.cloud/api" npx @modelcontextprotocol/inspector uv --directory . run youtrack-mcp
```

Este comando:
- Inicia un servidor proxy en el puerto 6277
- Proporciona una interfaz web en el puerto 6274
- Permite probar todas las herramientas MCP disponibles
- Facilita el debugging de mensajes entre cliente y servidor
- Genera un token de sesión para autenticación

### Variables de Entorno Requeridas
Las variables se configuran antes de ejecutar el servidor:
- `YOUTRACK_API_TOKEN`: Token de API de YouTrack
- `YOUTRACK_BASE_URL`: URL base de la API de YouTrack

### Requisitos Previos
- Node.js y npm instalados en WSL (no usar versiones de Windows)
- uv instalado para gestión de dependencias Python
- Acceso a la instancia de YouTrack configurada

### Casos de Prueba Recomendados
1. **Conexión básica**: Verificar que el servidor MCP se inicia correctamente
2. **Herramientas disponibles**: Listar todas las herramientas expuestas por el servidor
3. **Autenticación**: Verificar que las credenciales de YouTrack funcionan
4. **Operaciones CRUD**: Probar lectura de issues, tareas, comentarios
5. **Manejo de errores**: Verificar comportamiento con datos inválidos

### Alternativas de Prueba
```bash
# Ejecución directa del servidor (para debugging)
env YOUTRACK_BASE_URL="https://tu-instancia.youtrack.cloud/api" YOUTRACK_API_TOKEN="tu-token-de-api" python3 main.py

# Configuración con argumentos opcionales
env YOUTRACK_BASE_URL="https://tu-instancia.youtrack.cloud/api" YOUTRACK_API_TOKEN="tu-token-de-api" python3 main.py --timeout 30 --finished-states "Done,Closed"
```

### Obtención de credenciales
- **Token de API**: Generar en YouTrack → Profile → Authentication → New token
- **URL base**: Formato `https://tu-instancia.youtrack.cloud/api` (sin trailing slash)