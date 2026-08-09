# Guía de Arquitecturas Candidatas

Esta guía establece el proceso para **evaluar múltiples arquitecturas candidatas antes de comprometerse con una**. El objetivo no es generar documentación burocrática, sino asegurar que la decisión arquitectónica está fundamentada en trade-offs explícitos, no en preferencias personales ni en "así lo hace todo el mundo".

---

## Cuándo activar este proceso

Actívalo **siempre** en Caso A y Caso C (greenfield y TO-BE). En Caso B (AS-IS) solo si el usuario pide explícitamente evaluar alternativas a lo implementado.

**No necesitas evaluar 5 alternativas si solo 2 son viables.** Evalúa las que tengan mérito real. Si una opción es claramente inferior en todos los criterios, descártala rápido y documenta por qué en una línea — no le dediques una sección completa.

---

## Proceso de evaluación

### Paso 1 — Identificar drivers arquitectónicos

Antes de proponer cualquier arquitectura, extrae los **drivers** (fuerzas que moldean la arquitectura) del `.md` de especificaciones y de la línea base (Paso 0.5):

1. **Drivers funcionales**: los 2-4 casos de uso más críticos para el negocio.
2. **Drivers de calidad (atributos no funcionales priorizados)**: ¿qué es más importante? ¿latencia < 100ms o consistencia fuerte? ¿time-to-market en 2 meses o escalar a 10M usuarios?
3. **Restricciones**: presupuesto, stack obligatorio, equipo actual, proveedor de nube, compliance.
4. **Supuestos**: lo que asumes pero no está confirmado.

Documenta esto en la **Sección 3 del documento** (Drivers Arquitectónicos) antes de pasar a candidatas.

### Paso 2 — Generar 2-4 arquitecturas candidatas

Para cada candidata, describe en **máximo una página** (diagrama C4 nivel Contenedores + texto conciso):

| Elemento | Descripción |
|---|---|
| **Nombre** | Etiqueta descriptiva: "Monolito Modular con PostgreSQL" o "Microservicios en AWS ECS + EventBridge" |
| **Estilo(s) arquitectónico(s)** | Monolito modular, microservicios, serverless, event-driven, CQRS, hexagonal, space-based, etc. |
| **Diagrama C4 Contenedores** | Mermaid embed. Muestra los 3-8 contenedores principales y sus interacciones. |
| **Decisiones clave** | 3-5 bullets: ¿qué DB y por qué? ¿cómo se comunican los servicios (sync HTTP, async eventos, gRPC)? ¿cómo se autentica? ¿cómo escala? |
| **Trade-offs explícitos** | ¿Qué GANAS con esta arquitectura? ¿Qué PIERDES o qué riesgo ASUMES? |

### Paso 3 — Evaluar con matriz de decisión ponderada

Usa esta matriz para comparar las candidatas. Los pesos dependen del proyecto — ajústalos según los drivers del Paso 1:

| Criterio | Peso | Candidata A | Candidata B | Candidata C |
|---|---|---|---|---|
| **Time-to-market** (velocidad de desarrollo inicial) | XX% | 1-5 | 1-5 | 1-5 |
| **Escalabilidad** (horizontal, elasticidad bajo carga) | XX% | 1-5 | 1-5 | 1-5 |
| **Mantenibilidad** (facilidad de cambiar/extender, onboarding) | XX% | 1-5 | 1-5 | 1-5 |
| **Costo operativo** (infraestructura + equipo para operar) | XX% | 1-5 | 1-5 | 1-5 |
| **Resiliencia** (tolerancia a fallos, recuperación, disaster recovery) | XX% | 1-5 | 1-5 | 1-5 |
| **Seguridad** (superficie de ataque, aislamiento, compliance) | XX% | 1-5 | 1-5 | 1-5 |
| **Alineación con equipo actual** (stack conocido, curva de aprendizaje) | XX% | 1-5 | 1-5 | 1-5 |
| **Flexibilidad futura** (capacidad de evolucionar sin reescribir) | XX% | 1-5 | 1-5 | 1-5 |
| **TOTAL PONDERADO** | 100% | X.X | X.X | X.X |

**Escala de puntuación:**
- **5**: Excelente — esta arquitectura sobresale en este criterio, es una ventaja competitiva.
- **4**: Buena — cumple bien, sin fricción significativa.
- **3**: Adecuada — funciona pero hay opciones mejores.
- **2**: Deficiente — presenta problemas conocidos en este criterio.
- **1**: Inviable — este criterio bloquea esta arquitectura.

### Paso 4 — Recomendar con justificación

Tras la matriz, selecciona la arquitectura recomendada y explica **por qué** en términos de los drivers, no solo "ganó en el puntaje". Ejemplo de buena justificación:

> *Se recomienda la Candidata B (Monolito Modular con PostgreSQL) porque para los primeros 12 meses el driver principal es time-to-market con un equipo de 3 desarrolladores full-stack. La Candidata A (Microservicios) puntúa mejor en escalabilidad pero introduce una complejidad operativa que el equipo actual no puede absorber sin contratar 2 DevOps dedicados. Se establece como trigger de reevaluación: cuando el sistema supere 50K usuarios activos diarios, reconsiderar extraer el módulo de notificaciones como servicio independiente (Strangler Fig).*

---

## Anti-patrones a evitar

1. **"La arquitectura de moda"**: No elijas microservicios porque "todo el mundo los usa" — si tu equipo es de 3 personas y el dominio no es complejo, un monolito modular es la decisión correcta y no tenés que pedir disculpas por eso.
2. **Parálisis por análisis**: Presentar 7 alternativas con 15 criterios cada una. Si llegás a eso, es que los drivers no están claros — volvé al Paso 1.
3. **Falsa objetividad**: Manipular los pesos para que "gane" la arquitectura que ya decidiste antes de hacer la matriz. La matriz es una herramienta de pensamiento, no un justificante de decisiones pre-tomadas.
4. **Ignorar al equipo**: La mejor arquitectura del mundo es mala si el equipo no puede implementarla. El criterio "Alineación con equipo actual" debe tener peso real.

---

## Cómo documentarlo en el entregable final

En el `Documento_Arquitectura_<Proyecto>.md`, incluye:

```
## 4. Arquitecturas Candidatas Evaluadas

### 4.1 Drivers Arquitectónicos
[Resumen de la Sección 3 con los 3-5 drivers principales priorizados]

### 4.2 Candidata A: [Nombre]
[Diagrama C4 Contenedores en Mermaid]
[Decisiones clave, trade-offs]

### 4.3 Candidata B: [Nombre]
[Diagrama C4 Contenedores en Mermaid]
[Decisiones clave, trade-offs]

### 4.4 Candidata C: [Nombre] (si aplica)
[Diagrama C4 Contenedores en Mermaid]
[Decisiones clave, trade-offs]

### 4.5 Matriz de Decisión
[Tabla con pesos, puntuaciones y total ponderado]

### 4.6 Arquitectura Seleccionada
[Cuál se eligió, por qué, y triggers de reevaluación si los hay]

### 4.7 Alternativas Descartadas
[Si alguna opción obvia se descartó rápido sin evaluación completa, mencionarla acá con el motivo en una línea — ej. "Serverless puro: descartado por requisito de latencia < 50ms con cold start de Lambda"]
```

---

## Relación con ADRs

Si la decisión entre candidatas fue particularmente reñida o tiene implicaciones de largo plazo, genera un ADR (Architecture Decision Record) en `resources/architecture/adr/ADR-001-seleccion-arquitectura.md` documentando:

- **Contexto**: qué problema resolvemos y qué drivers lo moldean
- **Decisión**: qué arquitectura elegimos
- **Alternativas consideradas**: las otras candidatas y por qué se descartaron
- **Consecuencias**: lo que ganamos, lo que perdemos, lo que monitoreamos para reevaluar
