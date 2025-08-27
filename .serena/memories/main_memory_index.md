# Youtrack-MCP: Guía de Memorias del Proyecto

## 📚 Punto de entrada principal para entender y trabajar con el proyecto

Esta es la memoria principal que te ayudará a navegar por toda la documentación del proyecto Youtrack-MCP. Léela primero para entender qué memorias están disponibles y cuándo usar cada una.

## 🎯 ¿Qué tipo de tarea vas a realizar?

### 🏗️ **Para entender la arquitectura del proyecto**
**Lee:** `architecture_class_responsibilities`
- **Cuándo:** Necesitas entender qué hace cada clase y módulo
- **Contiene:** Responsabilidades detalladas de cada archivo, flujo de datos entre componentes
- **Útil para:** Debugging, refactoring, añadir nuevas funcionalidades complejas

### 🔧 **Para hacer cambios en el código**
**Lee:** `development_change_guide`
- **Cuándo:** Vas a implementar nuevas funcionalidades o modificar existentes
- **Contiene:** Guía práctica de dónde hacer cada tipo de cambio, flujos típicos
- **Útil para:** Saber exactamente qué archivo modificar según lo que quieras implementar

### 📋 **Para entender el overview general**
**Lee:** `project_overview`
- **Cuándo:** Primera vez trabajando con el proyecto o necesitas contexto general
- **Contiene:** Propósito, tech stack, herramientas disponibles, casos de uso
- **Útil para:** Onboarding, explicar el proyecto a otros, decisiones de arquitectura

### 🎨 **Para seguir las convenciones de código**
**Lee:** `style_and_conventions`
- **Cuándo:** Escribiendo código nuevo o revisando código existente
- **Contiene:** Estilo de código real del proyecto, patterns utilizados, convenciones
- **Útil para:** Code reviews, mantener consistencia, onboarding de desarrolladores

### 🧪 **Para probar el proyecto**
**Lee:** `testing_procedures`
- **Cuándo:** Necesitas validar cambios o probar funcionalidades
- **Contiene:** Cómo usar Inspector MCP, casos de prueba, configuración de testing
- **Útil para:** QA, debugging, validación de funcionalidades

## 🚀 **Flujos de trabajo típicos**

### **Soy nuevo en el proyecto:**
1. `project_overview` → Entender qué hace el proyecto
2. `architecture_class_responsibilities` → Entender cómo está estructurado
3. `style_and_conventions` → Conocer las convenciones de código
4. `testing_procedures` → Aprender a probarlo

### **Quiero añadir una nueva herramienta MCP:**
1. `development_change_guide` → Ver el flujo para nuevas herramientas
2. `architecture_class_responsibilities` → Entender qué módulos tocar
3. `style_and_conventions` → Seguir las convenciones al escribir código
4. `testing_procedures` → Validar que funciona correctamente

### **Tengo un bug o problema:**
1. `architecture_class_responsibilities` → Entender el componente afectado
2. `testing_procedures` → Reproducir y debuggear el problema
3. `development_change_guide` → Saber dónde hacer el fix

### **Quiero hacer refactoring:**
1. `architecture_class_responsibilities` → Entender las dependencias
2. `development_change_guide` → Planificar los cambios
3. `style_and_conventions` → Mantener consistencia
4. `testing_procedures` → Validar que no rompí nada

## 📖 **Estructura de memorias del proyecto**

```
memorias/
├── 📌 main_memory_index (ESTA MEMORIA) - Punto de entrada
├── 🌟 project_overview - Overview general del proyecto  
├── 🏗️ architecture_class_responsibilities - Arquitectura detallada
├── 🔧 development_change_guide - Guía práctica para cambios
├── 🎨 style_and_conventions - Convenciones de código
└── 🧪 testing_procedures - Procedimientos de testing
```

## 💡 **Consejos para usar las memorias**

- **No leas todas las memorias a la vez** - ve directamente a la que necesitas según tu tarea
- **Combina memorias** - por ejemplo, `development_change_guide` + `style_and_conventions` al escribir código
- **Actualiza memorias** - si encuentras información desactualizada, actualízala
- **Usa como referencia** - no memorices todo, consulta cuando lo necesites

## 🔄 **Estado actual del proyecto**

- **Herramientas MCP disponibles:** `getTasksInformation`, `getIssueById`
- **Arquitectura:** Modular con separación clara de responsabilidades
- **Tech stack:** Python 3.12+, requests, mcp, uv
- **Testing:** Inspector MCP para validación interactiva
- **Estado:** Funcional y listo para producción

---

**🎯 Siguiente paso:** Identifica qué tipo de tarea vas a realizar y lee la memoria correspondiente según la guía anterior.