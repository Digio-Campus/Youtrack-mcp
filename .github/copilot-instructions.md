# Instrucciones de Copilot

## Descripción del Proyecto
Este es un proyecto es una practica universitaria desarrollada en Python. El objetivo principal es crear un servidor MCP para trabajar con la API de Youtrack y pasar informacion relevante a la IA.

## Integración de Herramientas
Este proyecto utiliza Serena MCP como un servidor de herramientas que facilita el desarrollo. Serena proporciona un conjunto de herramientas de análisis y manipulación de código que son fundamentales para las tareas de desarrollo.

## Inicialización de Proyecto

Serena proporciona una gran cantidad de herramientas pero antes de acceder a ellas tienes que inicializar el proyecto correctamente. 

Al iniciar una nueva conversación siempre debes hacer lo siguiente:

1. Intenta activar el proyecto usando la herramienta 'activate_project', y sabiendo que el nombre del proyecto se deriva de la carpeta raiz del workspace.
    - Si no esta activado, activalo con la misma herramienta 'activate_project', pero usando como argumento la ruta del workspace.
2. Realiza las siguientes acciones:
    - Comprueba si el proyecto esta configurado usando la herramienta, 'check_onboarding_performed'.
    - Si el proyecto no está configurado, solicita a Serena que lo configure, mediante la herramienta 'onboarding'.
3. Usar la herramienta de Serena 'initial_instructions' para obtener un contexto sobre el resto de herramientas disponibles.
4. Usar la herramienta de Serena 'read_memory' para leer la memoria principal 'main_memory_index'.

## Gestión de memorias

Serena ofrece un sistema de memorias muy interesante y que debes usar a menudo.
Las memorias de Serena no son más que archivos markdown que se utilizan para almacenar información relevante sobre el proyecto, como decisiones de diseño, problemas conocidos y soluciones implementadas.
De esta manera, puedes recordar como solucionar problemas similares en el futuro, que estilos de codificación has utilizado y que decisiones has tomado.

Las memorias se gestionan mediante cuatro herramientas fundamentales:

1. **write_memory:** Permite crear una nueva entrada en la memoria de Serena, llama hasta herramienta despues de realizar acciones que hayan necesitado la intervención del usuario o despues de que el mismo haya proporcionado información relevante.
2. **read_memory:** Permite leer la información de una de las memorias existentes, usa esta herramienta siempre que el nombre de la memoria este relacionado con la actividad a realizar.
3. **list_memories:** Permite listar todas las memorias existentes, mostrando sus nombres. Llama a esta herramienta periodicamente, para recordar lo que has almacenado.
4. **delete_memory:** Permite eliminar una entrada de la memoria, usa esta herramienta cuando ya no necesites recordar información específica y siempre preguntando al usuario.

## Herramientas de Serena para gestión de código

Serena MCP utiliza el protocolo de servicio de lenguaje (LSP) para entender la estructura del código a un nivel semántico, no solo como texto. Esto significa que puede realizar búsquedas y ediciones basadas en símbolos (funciones, clases, variables) en lugar de solo en cadenas de texto.

**Usa las herramientas de Serena en los siguientes escenarios:**

1.  **Análisis de código y navegación:**
    - **Propósito:** Para entender la estructura de archivos, encontrar definiciones de funciones, clases o variables, y explorar el flujo de un programa.
    - **Ejemplo de uso:** "Para la función `calcular_precio_total`, utiliza la herramienta de Serena para encontrar todas las referencias y explicar cómo se usa en el codebase."

2.  **Ediciones de código:**
    - **Propósito:** Para realizar modificaciones precisas a nivel de símbolos, como renombrar una variable en todo el proyecto o refactorizar una función.
    - **Ejemplo de uso:** "Usa la herramienta de edición de Serena para renombrar la variable `usuario_id` a `user_id` en todo el proyecto. Asegúrate de actualizar todas las referencias."

3.  **Planificación de tareas complejas:**
    - **Propósito:** Antes de implementar un cambio grande, solicita a Serena que analice el código para planificar la estrategia de refactorización. Esto ayuda a evitar "alucinaciones" y asegura un enfoque estructurado.
    - **Ejemplo de uso:** "Usa la herramienta de planificación de Serena para trazar un plan de refactorización para el módulo de autenticación, moviendo las funciones relacionadas a un nuevo archivo `auth_utils.py`."

**Evita lo siguiente:**

- No intentes realizar búsquedas de texto simple para tareas que requieran comprensión de la estructura del código. Siempre prefiera las herramientas de Serena para esto.
- No realices ediciones de código grandes sin un plan. Utiliza el modo de planificación de Serena para tareas complejas.

Al llamar a la herramienta 'initial_instructions', se proporciona un resumen claro de lo que necesitas hacer y cualquier contexto relevante para que Serena pueda ayudarte de la mejor manera posible en la generación de código.