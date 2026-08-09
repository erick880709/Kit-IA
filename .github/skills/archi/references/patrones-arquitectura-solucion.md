# Catálogo de Patrones de Arquitectura de Solución

Patrones que resuelven problemas recurrentes a nivel de solución enterprise, infraestructura cloud y diseño de integraciones. Complementan los patrones de software del catálogo `patrones-arquitectura-software.md`.

---

## Patrones de Integración Enterprise (EIP)

### 1. API Gateway / Backend for Frontend (BFF)

```
[Mobile App] ──→ [BFF Mobile] ──→ [Microservicios]
[Web SPA]    ──→ [BFF Web]    ──→ [Microservicios]
[Third Party]──→ [API Gateway público]
```

**Decisión clave:** ¿Un solo API Gateway para todos los clientes, o un BFF por cliente?
- **API Gateway único**: Más simple, pero la API queda acoplada a las necesidades de todos los clientes. Sirve para APIs públicas o cuando mobile/web necesitan los mismos datos.
- **BFF por cliente**: Cada cliente (mobile, web, third-party) tiene su propio backend ligero que agrega/excluye datos según lo que ese cliente necesita. Evita over-fetching y under-fetching.

**Productos:** AWS API Gateway + Lambda@Edge, Azure API Management, Apigee, Kong, Envoy.

### 2. Message Broker / Event Bus

**Decisión clave:** ¿Colas punto-a-punto o pub/sub?

| Patrón | Producto | Mejor para |
|---|---|---|
| **Colas (Point-to-Point)** | SQS, Azure Queue Storage, RabbitMQ | Distribuir trabajo entre workers, garantizar procesamiento exact-once |
| **Pub/Sub** | SNS + SQS, EventBridge, Pub/Sub, Kafka | Notificar a múltiples consumidores del mismo evento, desacoplar productores de consumidores |
| **Event Streaming** | Kafka, Kinesis, Event Hubs | Replay de eventos, orden garantizado, alta throughput, retención larga |

### 3. Transactional Outbox

**Problema:** ¿Cómo publicar un evento a un broker solo si la transacción de DB se confirma, sin usar distributed transactions (2PC/XA)?

**Solución:**
```
1. Escribir evento en tabla "outbox" dentro de la misma transacción que modifica la entidad
2. Un proceso (poller/CDC) lee la tabla outbox y publica al broker
3. Marcar como publicado; eliminar tras ventana de retención
```

**Cuándo usarlo:** SIEMPRE que necesites garantía "al menos una vez" entre DB y mensajería. No usar 2PC: no escala y crea acoplamiento.

**Productos:** Debezium + Kafka Connect (CDC), AWS DMS + Kinesis, Cloud SQL + Pub/Sub.

---

## Patrones de Datos

### 4. Database per Service (Microservicios)

Cada microservicio es dueño de sus datos. Otros servicios acceden SOLO vía API. **No compartas DB entre servicios** — crea un acoplamiento invisible que anula los beneficios de los microservicios.

**Excepciones válidas (documentar como ADR):**
- Migración gradual (Strangler Fig): dos servicios comparten temporalmente la DB vieja mientras se migran datos.
- Reporting: un servicio replica datos de varios servicios en una DB de solo-lectura para analytics. Es válido si es explícito y los servicios fuente son los dueños.

### 5. CQRS con Event Sourcing

```
[Command] → [Aggregate] → [Evento(s)] → [Event Store] → [Proyección(es)] → [Query]
```

Cada cambio de estado es un evento inmutable guardado en secuencia. El estado actual se deriva reproduciendo eventos. Las proyecciones son vistas materializadas optimizadas para lectura.

**Cuándo sí:** Auditoría completa obligatoria, reconstrucción de estado a cualquier punto en el tiempo, dominios con eventos naturales (contabilidad, logística).

**Cuándo no:** CRUD simple, equipos sin experiencia (la curva de aprendizaje es alta), necesidad de consistencia fuerte en lecturas inmediatas.

### 6. Data Lakehouse

```
[Data Sources] → [Bronze Layer: raw data en formato nativo] → [Silver Layer: datos limpiados y validados] → [Gold Layer: datos agregados listos para consumo]
                    ↓                                                      ↓
              (Object Storage: S3, ADLS, GCS)                      (Query Engine: Athena, Databricks SQL, BigQuery)
```

Arquitectura medallón (bronze/silver/gold) para pipelines de datos analíticos. Combina la flexibilidad del data lake (formatos abiertos: Parquet, Iceberg, Delta Lake) con capacidades de data warehouse (SQL, ACID en tablas).

**Productos:** Databricks (Delta Lake), Apache Iceberg + Athena/Trino, Microsoft Fabric, BigLake.

---

## Patrones de Seguridad

### 7. Zero Trust Architecture (ZTA)

Principio: **"Nunca confíes, siempre verifica."** A diferencia del modelo de perímetro (firewall protege la red interna y dentro todo es confiable), ZTA asume que la red está comprometida y verifica cada request individualmente.

**Componentes clave:**
- **Identity-aware proxy**: Cada request requiere autenticación (OAuth2/OIDC), sin importar si viene de "adentro" o "afuera".
- **mTLS entre servicios**: Todos los servicios se comunican con TLS mutuo (certificados de cliente).
- **Políticas de acceso basadas en atributos (ABAC)**: No solo el rol, sino ubicación, dispositivo, horario, sensibilidad del dato.

**En la práctica cloud:** AWS IAM + API Gateway con autorizador Cognito, Azure AD + API Management, BeyondCorp-style con Identity-Aware Proxy (GCP).

### 8. Sidecar para Seguridad (Service Mesh)

En vez de que cada microservicio implemente mTLS, rate limiting y circuit breaking en su código, un sidecar proxy (Envoy/Istio, Linkerd) maneja todo eso en la capa de infraestructura. El código de aplicación se mantiene simple y el equipo de plataforma gestiona la seguridad.

**Cuándo usarlo:** Más de 5 microservicios en Kubernetes. Para menos, el overhead de operar un service mesh no se justifica — implementá mTLS a nivel de aplicación con librerías.

---

## Patrones de Cloud-Native

### 9. Serverless / FaaS primero

Priorizar servicios gestionados sin servidor (Lambda, Cloud Run, Azure Functions) antes que contenedores auto-gestionados. **Regla de decisión:**

- **Usar serverless si:** Tráfico variable/impredecible, time-to-market es prioridad, equipo pequeño sin experiencia en Kubernetes.
- **Usar contenedores (ECS/Fargate, GKE, AKS) si:** Necesitás control fino sobre el runtime, tráfico estable y predecible (menor costo), latencia de cold start inaceptable para tu caso de uso.

### 10. Event Sourcing con Serverless (CQRS + FaaS)

```
[API Gateway] → [Lambda: Command Handler] → [DynamoDB Streams] → [Lambda: Projector] → [DynamoDB (Read Model)] → [Lambda: Query Handler]
```

Arquitectura serverless completa para CQRS: DynamoDB Streams como event bus, Lambdas como procesadores, DynamoDB como event store y read model. Bajo costo operativo, escala a cero cuando no hay tráfico.

**Limitación:** DynamoDB Streams retiene eventos solo 24h. Para retención más larga, usar Kinesis Data Streams en su lugar.

---

## Patrones de Observabilidad

### 11. Distributed Tracing

En un sistema con múltiples servicios, un request de usuario puede tocar 5-10 servicios. Sin tracing, debuggear latencia o errores es casi imposible.

**Stack estándar:**
- **Instrumentación:** OpenTelemetry SDK (vendor-neutral, soporta todos los backends)
- **Recolección:** OpenTelemetry Collector (sidecar o daemon)
- **Backend:** AWS X-Ray, Azure Monitor (Application Insights), Google Cloud Trace, Jaeger, Grafana Tempo
- **Visualización:** Grafana, AWS CloudWatch ServiceLens, Azure Monitor

**Estándar de propagación de contexto:** W3C Trace Context (`traceparent` header). Todos los servicios deben propagarlo — si un servicio lo rompe, el trace se fragmenta.

### 12. Health Check API

TODO servicio (monolito o microservicio) debe exponer:
- `GET /health` — ¿está vivo? (liveness: ¿respondió el proceso?)
- `GET /health/ready` — ¿puede recibir tráfico? (readiness: ¿DB conectada? ¿dependencias arriba?)
- `GET /health/startup` — ¿terminó de inicializar? (startup: para apps que tardan en cargar, evita que el orchestrator las mate por lentas)

**En Kubernetes:** `livenessProbe` → `/health`, `readinessProbe` → `/health/ready`, `startupProbe` → `/health/startup`.

---

## Anti-Patrones de Solución (qué NO hacer)

| Anti-Patrón | Descripción | Cómo evitarlo |
|---|---|---|
| **Distributed Monolith** | Microservicios que comparten DB o requieren despliegues coordinados. Peor que un monolito: tenés la complejidad de red + el acoplamiento de monolito. | Database per service, contratos de API versionados, despliegue independiente. |
| **Death Star** | Tantos microservicios interdependientes que el grafo de llamadas es imposible de entender. | Limitar dependencias, usar eventos async, service mesh para visibilidad. |
| **Big Ball of Mud (cloud)** | Migrar un monolito legacy "levantando y corriendo" a la nube sin refactorizar. Terminás pagando más por lo mismo. | Strangler Fig, refactorizar por bounded context ANTES de migrar. |
| **Vendor Lock-in por comodidad** | Usar tantos servicios propietarios sin abstracción que migrar de nube cuesta reescribir. | Para componentes no diferenciadores (cola de mensajes, cache), preferir protocolos abiertos (AMQP, Redis wire protocol). Para componentes core del negocio, la abstracción puede ser peor que el lock-in — documentar la decisión como ADR. |
| **Over-engineering prematuro** | Prepararse para 10M de usuarios cuando tenés 100. Escalar cuando lo necesites, no antes. | YAGNI: You Aren't Gonna Need It. Arquitectura que escala horizontalmente con un feature toggle, no con una reescritura. |
