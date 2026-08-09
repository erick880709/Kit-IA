# Guía de Descomposición de Épicas

## Tabla de Contenidos
1. [Cuántas historias generar](#cuántas-historias)
2. [Historia de Usuario vs. Tarea Técnica](#hu-vs-tt)
3. [Patrones de descomposición](#patrones)
4. [Criterios de Aceptación bien escritos](#criterios-de-aceptación)
5. [Estimación de Story Points](#estimación)
6. [Épicas ambiguas](#épicas-ambiguas)
7. [Ejemplos por tipo de épica](#ejemplos)

---

## Cuántas historias

| Tamaño épica (por descripción) | Historias sugeridas | Tareas técnicas |
|---|---|---|
| Pequeña (1-2 párrafos, flujo simple) | 2–4 | 1–2 |
| Mediana (flujo con variantes, múltiples roles) | 4–8 | 2–4 |
| Grande (múltiples módulos, integraciones) | 8–15 | 4–8 |

Si el resultado supera 15 historias, proponer dividir la épica en dos o más.

---

## HU vs TT

### Historia de Usuario — criterios para clasificar como HU:
- El usuario final la puede ver, usar o recibir valor directo de ella
- Se puede escribir en formato "Como [rol], quiero [qué], para [por qué]"
- Tiene criterios de aceptación funcionales verificables por QA

### Tarea Técnica — criterios para clasificar como TT:
- Es trabajo de infraestructura, arquitectura o deuda técnica
- El usuario final no la percibe directamente
- Ejemplos típicos:
  - Crear/migrar esquema de base de datos
  - Configurar pipeline CI/CD
  - Crear endpoints de API (sin UI)
  - Refactorización o setup de frameworks
  - Configurar permisos/roles a nivel de sistema
  - Integración con servicios externos (sin UI)
  - Documentación técnica o de APIs

---

## Patrones de Descomposición

### Patrón 1: Por pasos del flujo de usuario (más común)
Divide el flujo principal en etapas:
- Registro / Autenticación
- Configuración / Setup inicial
- Operación principal (CRUD)
- Visualización / Reportes
- Notificaciones / Comunicaciones

### Patrón 2: Por rol de usuario
Cuando hay múltiples actores:
- HU para el rol Admin
- HU para el rol Usuario Final
- HU para el rol Supervisor/Manager

### Patrón 3: Por variante o edge case
- HU del happy path
- HU de manejo de errores / casos límite
- HU de permisos / validaciones

### Patrón 4: Por canal o dispositivo
- HU para Web
- HU para Mobile
- HU para API externa / integración

### Patrón 5: MVP primero
Divide en:
- HU mínimas para lanzar (MVP)
- HU de mejora / fase 2
Etiquétalas claramente.

---

## Criterios de Aceptación bien escritos

**Formato recomendado (Gherkin simplificado):**
```
Dado [contexto/precondición]
Cuando [acción del usuario]
Entonces [resultado esperado]
```

**O lista de verificación directa:**
```
- [ ] El campo X es obligatorio y muestra error si está vacío
- [ ] El sistema envía email de confirmación en menos de 2 minutos
- [ ] La lista pagina de a 20 registros
```

**Anti-patrones a evitar:**
- ❌ "El sistema funciona bien" (no verificable)
- ❌ "Es rápido" (sin métrica)
- ❌ "El usuario puede hacer todo lo necesario" (ambiguo)

**Buenas prácticas:**
- ✅ Incluir al menos 2 y máximo 6 criterios por historia
- ✅ Criterios de errores y validaciones explícitos
- ✅ Mencionar umbrales concretos (tiempo, cantidad, tamaño)

---

## Estimación de Story Points (Fibonacci)

| Puntos | Complejidad | Ejemplo |
|---|---|---|
| 1 | Trivial, sin lógica | Cambiar texto de un botón |
| 2 | Simple, lógica mínima | Agregar campo a formulario existente |
| 3 | Pequeño, lógica clara | CRUD simple de una entidad |
| 5 | Mediano, algunas variantes | Flujo con validaciones y estados |
| 8 | Complejo, múltiples casos | Integración con API externa + manejo de errores |
| 13 | Muy complejo, incertidumbre alta | Considerar dividir |

Regla: Si llegas a 13, probablemente hay que dividir la historia.

---

## Épicas Ambiguas

Cuando la épica tiene descripción insuficiente, sigue este protocolo:

### Señales de épica ambigua:
- Descripción menor a 3 oraciones
- Sin mención de usuarios/roles específicos
- Sin criterios de éxito ni restricciones
- Solo tiene el título

### Preguntas clave a hacer (máximo 3 a la vez):

**Sobre el usuario:**
- ¿Quiénes son los usuarios que interactuarán con esta funcionalidad?
- ¿Hay diferentes roles con permisos distintos?

**Sobre el flujo:**
- ¿Cuál es el flujo principal que debe poder completar el usuario?
- ¿Existen sistemas externos con los que debe integrarse?

**Sobre el alcance:**
- ¿Hay alguna funcionalidad que explícitamente queda fuera?
- ¿Existe una fecha de entrega o restricción técnica importante?

### Generar borrador con supuestos:
Si el usuario no puede o no quiere responder preguntas, genera las historias igual pero:
1. Encabeza con: `⚠️ Análisis basado en supuestos — requiere validación`
2. Lista los supuestos explícitamente antes del desglose
3. Marca con 🔶 las historias con mayor incertidumbre

---

## Ejemplos por tipo de épica

### Épica de Autenticación/Acceso
**Historias típicas:**
- HU: Registro de nuevo usuario con email
- HU: Login con usuario y contraseña
- HU: Recuperación de contraseña
- HU: Login con proveedor OAuth (Google/Microsoft)
- TT: Implementar JWT / sistema de sesiones
- TT: Configurar políticas de seguridad de contraseñas

### Épica de Gestión de Entidad (CRUD)
**Historias típicas:**
- HU: Crear nuevo [entidad]
- HU: Listar y buscar [entidades]
- HU: Ver detalle de [entidad]
- HU: Editar [entidad]
- HU: Archivar/eliminar [entidad]
- TT: Diseñar y migrar esquema de BD
- TT: Crear endpoints REST para [entidad]

### Épica de Reportes/Dashboard
**Historias típicas:**
- HU: Ver resumen ejecutivo con KPIs
- HU: Filtrar datos por rango de fechas
- HU: Exportar reporte a PDF/Excel
- HU: Configurar alertas por umbral
- TT: Crear capa de agregación/analytics en BD
- TT: Integrar librería de gráficos

### Épica de Notificaciones
**Historias típicas:**
- HU: Recibir notificación por email al [evento X]
- HU: Ver centro de notificaciones en la app
- HU: Configurar preferencias de notificaciones
- TT: Integrar servicio de email (SendGrid, SES, etc.)
- TT: Implementar sistema de colas para envíos masivos
