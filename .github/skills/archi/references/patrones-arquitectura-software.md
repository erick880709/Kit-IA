# Catálogo de Patrones de Arquitectura de Software

Este catálogo describe patrones arquitectónicos a nivel de sistema y de componente. Úsalo como referencia al proponer arquitecturas (Casos A y C) y al documentar sistemas existentes (Caso B). Cada patrón incluye cuándo usarlo, cuándo NO usarlo, y sus trade-offs.

---

## Patrones de Estructura (Organización del Código)

### 1. Arquitectura en Capas (Layered Architecture)

```
Presentación → Aplicación → Dominio → Infraestructura
```

**Cuándo usarlo:**
- Equipos que recién empiezan y necesitan una estructura simple de entender
- Aplicaciones CRUD con poca lógica de dominio compleja
- Proyectos donde la separación clara de responsabilidades por capa técnica es suficiente

**Cuándo NO usarlo:**
- Dominios complejos con reglas de negocio que cambian frecuentemente (las capas no protegen el dominio)
- Necesidad de cambiar la infraestructura sin tocar el dominio (la capa de arriba depende de la de abajo)

**Variantes:**
- **Capa de Servicio (Service Layer)**: Agregar una capa intermedia entre aplicación y dominio que orquesta casos de uso y maneja transacciones.
- **Capa de Anti-Corrupción (ACL)**: Capa que traduce entre el dominio interno y sistemas externos para que el modelo de dominio no se contamine.

---

### 2. Arquitectura Hexagonal (Ports & Adapters)

```
[Driver Adapters] → Ports (interfaces) → [Domain Core] ← Ports (interfaces) ← [Driven Adapters]
   (HTTP, CLI, Test)                       (lógica pura)                        (DB, API externa, Cola)
```

**Cuándo usarlo:**
- Necesitas testear la lógica de dominio sin infraestructura real (DB, APIs externas)
- Vas a cambiar la infraestructura (ej. migrar de PostgreSQL a MongoDB, o de REST a gRPC) sin reescribir el dominio
- Domain-Driven Design (DDD): el dominio es el corazón y la infraestructura es un detalle

**Cuándo NO usarlo:**
- Aplicaciones muy simples (CRUD de una sola entidad): el overhead de puertos/adaptadores no se justifica
- Equipos sin experiencia en inversión de dependencias (DIP de SOLID): mal implementado, termina siendo capas con otro nombre

**Conceptos clave:**
- **Puerto (Port)**: Interfaz que define una intención del dominio (ej. `UserRepository`, `NotificationSender`). No sabe nada de infraestructura.
- **Adaptador (Adapter)**: Implementación concreta que conecta un puerto con tecnología real (ej. `PostgresUserRepository`, `SnsNotificationSender`).
- **Driver side (lado izquierdo)**: Lo que usa el dominio (controladores HTTP, CLI commands, tests).
- **Driven side (lado derecho)**: Lo que el dominio usa (DB, APIs, message brokers).

---

### 3. Clean Architecture (Uncle Bob)

```
Frameworks → Interface Adapters → Application Use Cases → Enterprise Entities
(capa externa, web/DB)   (controllers, repos)   (casos de uso)       (entidades de dominio puras)
```

**Cuándo usarlo:**
- Sistemas enterprise con larga vida esperada (>5 años) donde la independencia de frameworks es prioritaria
- Múltiples interfaces de entrega para el mismo dominio (web, mobile, API, CLI)
- Necesidad de diferir decisiones de infraestructura (elegir la DB en mes 3, no en la semana 1)

**Cuándo NO usarlo:**
- MVPs o startups en fase de validación: el overhead estructural frena la iteración rápida
- Equipos pequeños (<4 devs) sin necesidad real de esta separación

**Diferencia con Hexagonal:** Clean Architecture especifica una estructura de capas concéntricas con regla de dependencia estricta (las capas internas no conocen las externas). Hexagonal es más flexible en la organización interna del dominio.

---

### 4. Arquitectura Modular (Modular Monolith)

```
Módulo A (Pedidos)    Módulo B (Inventario)    Módulo C (Facturación)
       ↓                      ↓                       ↓
         Capa compartida de infraestructura (DB, mensajería, logging)
```

**Cuándo usarlo:**
- **La mejor primera arquitectura para el 80% de los proyectos nuevos.** Combina simplicidad de despliegue (un solo artefacto) con organización por dominio (módulos con baja acoplamiento).
- Equipos de 3-15 desarrolladores que pueden crecer a mediano plazo
- Dominios que tienen claros límites de bounded context pero no justifican el costo operativo de microservicios todavía

**Cuándo NO usarlo:**
- Necesidad de escalar partes del sistema independientemente (si un módulo recibe 100x más tráfico que otro, considerar extraerlo a microservicio)
- Equipos independientes que necesitan desplegar en ciclos distintos y no pueden coordinar releases

---

### 5. Microservicios

**Cuándo usarlos:**
- Equipos independientes (8+ developers) que necesitan desplegar, escalar y fallar aisladamente
- Partes del sistema con requisitos de escalabilidad radicalmente distintos (un servicio de catálogo con 10K RPM vs un servicio de facturación con 10 RPM)
- Necesidad de polyglot persistence: cada servicio usa la DB óptima para su dominio

**Cuándo NO usarlos (aplica a la mayoría de los proyectos nuevos):**
- Equipos de menos de 8 personas: el costo de coordinación y DevOps supera los beneficios
- Dominios sin bounded contexts claros: microservicios mal acotados son peor que un monolito
- Startups pre-product-market-fit: la velocidad de iteración es prioridad #1

**Principios de diseño:**
- **Database per Service**: Cada microservicio es dueño de sus datos. Otros servicios solo acceden vía API (nunca directo a la DB).
- **Smart endpoints, dumb pipes**: La lógica está en los servicios, no en el bus/ESB. Preferí REST/gRPC + eventos sobre orquestación central.
- **Decentralized Governance**: Cada equipo elige su stack dentro de constraints razonables.

---

## Patrones de Comunicación

### 6. Event-Driven Architecture (EDA)

```
Servicio A ──(publica evento)──→ Message Broker ──(suscribe)──→ Servicio B
                                                    ──(suscribe)──→ Servicio C
```

**Cuándo usarlo:**
- Flujos de negocio que son naturalmente asíncronos (ej. "cuando se crea un pedido, notificar al almacén, facturar y enviar email")
- Necesidad de desacoplar servicios para que fallen independientemente
- Event Sourcing: reconstruir estado a partir de eventos inmutables
- Integración entre bounded contexts en DDD

**Trade-offs:**
- ✅ Alta resiliencia y desacoplamiento, escalabilidad independiente
- ❌ Debugging complejo (trazar un flujo a través de eventos), consistencia eventual (no apto para todo)

### 7. CQRS (Command Query Responsibility Segregation)

```
[Comandos (Write)] → Modelo de Escritura (normalizado, ACID) → [Eventos] → Modelo de Lectura (desnormalizado, read-optimized) → [Queries (Read)]
```

**Cuándo usarlo:**
- Discrepancia masiva entre lecturas y escrituras (ej. dashboard con 100 lecturas por segundo y 1 escritura por minuto)
- Necesidad de modelos de consulta radicalmente distintos al de escritura (search, reporting, analytics)
- Event Sourcing como fuente de verdad

**Cuándo NO usarlo:**
- CRUD simple donde lectura y escritura usan el mismo modelo
- Equipos pequeños: mantener dos modelos sincronizados tiene costo operativo

### 8. Saga Pattern (coordinación de transacciones distribuidas)

```
Saga = secuencia de transacciones locales, cada una con su compensación si algo falla

Orden Creada → Pago Reservado → Inventario Descontado → Envío Programado
     ↓ (si falla)       ↓ (si falla)         ↓ (si falla)
  Cancelar Orden    Liberar Pago        Restaurar Inventario
```

**Dos variantes:**
- **Coreografía**: Cada servicio reacciona a eventos y ejecuta su parte. Bueno para flujos simples (<5 pasos). Riesgo: lógica dispersa, difícil de entender el flujo completo.
- **Orquestación**: Un servicio coordinador central ejecuta la saga paso a paso. Bueno para flujos complejos o con muchas ramas condicionales. Riesgo: el orquestador se vuelve un monolito de lógica de negocio.

---

## Patrones de Resiliencia

### 9. Circuit Breaker

```
[Llamadas al servicio externo] → [Contador de fallos] → Si supera umbral → [Circuito ABIERTO: fallar rápido sin llamar]
                                  ↓ Periódicamente
                              [Circuito MEDIO-ABIERTO: permitir 1 llamada de prueba]
```

**Cuándo usarlo:** Toda llamada a un servicio externo que puede fallar o degradarse (APIs de terceros, microservicios, DBs). **No es opcional en microservicios — es obligatorio.**

### 10. Retry con Backoff Exponencial + Jitter

**Cuándo usarlo:** Errores transitorios (timeouts, rate limiting, deadlocks). **No usar** para errores de negocio (404, 401) — reintentar un "recurso no encontrado" no lo va a crear.

### 11. Bulkhead

Aislar recursos (thread pools, conexiones de DB) por funcionalidad para que un fallo en el módulo de reportes no tumbe el de pedidos. Cada módulo tiene su propio pool de conexiones a la DB, su propio thread pool.

---

## Patrones de Despliegue

### 12. Sidecar

**Qué es:** Un contenedor auxiliar que corre junto al contenedor principal en el mismo pod (Kubernetes) o task (ECS), compartiendo red y almacenamiento. Ejemplos: Envoy/Istio para service mesh, Cloud SQL Auth Proxy, logging agent.

### 13. Ambassador

**Qué es:** Proxy local que maneja comunicación con servicios externos (retry, circuit breaking, TLS). Diferencia con Sidecar: Ambassador media con el exterior; Sidecar extiende al contenedor principal.

### 14. Strangler Fig (migración incremental)

Migrar un monolito a microservicios extrayendo funcionalidad pieza por pieza, enrutando tráfico gradualmente del viejo al nuevo componente, hasta que el viejo queda sin uso y se elimina. Es la estrategia de migración recomendada por defecto sobre el "big bang rewrite".
