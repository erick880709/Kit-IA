# Guía de Selección de Bases de Datos

Esta guía proporciona un marco de decisión estructurado para elegir entre bases de datos relacionales y no relacionales, así como entre subtipos específicos. Debe aplicarse **antes** de diseñar la Sección 9 (Modelo de Datos) del documento de arquitectura.

---

## Árbol de decisión principal

```
¿Los datos tienen un esquema estable y conocible de antemano?
├── SÍ → ¿Necesito integridad referencial estricta (ACID)?
│   ├── SÍ → Base de Datos Relacional (SQL)
│   │   ├── OLTP transaccional → PostgreSQL, MySQL, SQL Server
│   │   ├── OLAP analítico → ClickHouse, Redshift, BigQuery
│   │   └── Mixto (HTAP) → PostgreSQL con particionado, CockroachDB, TiDB
│   └── NO → ¿Los datos son mayormente documentos JSON con estructura variable?
│       ├── SÍ → Document Store: MongoDB, Amazon DocumentDB, Azure Cosmos DB
│       └── NO → ¿Son grafos de relaciones complejas?
│           ├── SÍ → Graph DB: Neo4j, Amazon Neptune, Azure Cosmos DB Gremlin
│           └── NO → Wide-Column: Cassandra, ScyllaDB, Azure Cosmos DB Cassandra
└── NO (esquema fluido/impredecible) → ¿El patrón de acceso es clave-valor simple?
    ├── SÍ → Key-Value Store: Redis, DynamoDB (modo K/V), etcd
    └── NO → ¿Los datos son eventos inmutables en orden temporal?
        ├── SÍ → Event Store / Stream: Kafka, Kinesis, Event Hubs
        └── NO → ¿Son datos geoespaciales o de series temporales?
            ├── Geoespacial → PostGIS, MongoDB GeoJSON
            └── Series temporales → InfluxDB, TimescaleDB, Timestream
```

---

## Bases de Datos Relacionales (SQL)

### Cuándo elegirlas

- **Integridad transaccional obligatoria** (ACID): finanzas, inventario, órdenes, booking.
- **Consultas complejas con JOINs y agregaciones** frecuentes entre entidades relacionadas.
- **Esquema conocido y estable**: catálogos de productos, datos maestros, configuración.
- **Reporting y BI**: necesidad de SQL como lenguaje común del equipo de datos.
- **Cumplimiento normativo** que exige consistencia fuerte (GDPR data accuracy, SOX).

### Motores recomendados por caso de uso

| Motor | Mejor para | No usar para |
|---|---|---|
| **PostgreSQL** | Propósito general, JSON híbrido, GIS, full-text search, aplicaciones SaaS | Escrituras masivas >50K TPS sin particionado |
| **MySQL/MariaDB** | Aplicaciones web LAMP/LEMP clásicas, replicación simple | GIS avanzado, CTEs recursivos complejos |
| **SQL Server** | Ecosistema .NET, reporting integrado (SSRS/SSAS), Azure-native | Costo en self-hosted, licenciamiento complejo |
| **Oracle** | Enterprise legacy, RAC para HA, cargas financieras extremas | Startups (costo de licencia prohibitivo) |
| **CockroachDB** | SQL distribuido global, multi-región activo-activo | Aplicaciones simples single-region (overkill) |
| **PlanetScale** | MySQL serverless, branching de schemas tipo Git | Necesidades de stored procedures complejos |

### Patrones de diseño relacional

| Patrón | Descripción | Cuándo usarlo |
|---|---|---|
| **Normalización (3NF/BCNF)** | Eliminar redundancia, una entidad por tabla | OLTP, datos que cambian frecuentemente |
| **Desnormalización estratégica** | Duplicar datos selectivamente para velocidad de lectura | Reportes, dashboards, read-heavy workloads |
| **Particionado horizontal (sharding)** | Dividir tablas por rango de clave (tenant_id, fecha) | Multi-tenant SaaS, logs, series temporales en SQL |
| **CQRS a nivel de BD** | Separar modelo de escritura (normalizado) del de lectura (desnormalizado) | Alta discrepancia read/write, eventos sourcing |
| **Event Sourcing + SQL** | Guardar eventos en tabla inmutable, proyectar a vistas materializadas | Auditoría completa, reconstrucción de estado |

---

## Bases de Datos No Relacionales (NoSQL)

### 1. Document Stores (MongoDB, DocumentDB, Cosmos DB SQL API, Couchbase)

**Casos de uso ideales:**
- Catálogos de productos con atributos variables por categoría
- Perfiles de usuario con campos opcionales/extensibles
- Gestión de contenido (CMS): artículos, páginas con metadata variable
- Configuraciones por tenant en SaaS multi-tenant

**Cuándo NO usarlas:**
- Necesitas JOINs complejos entre colecciones (usa SQL o Graph)
- Transacciones multi-documento frecuentes (MongoDB 4.0+ las soporta, pero con costo)
- Reporting analítico pesado (mejor mover a data warehouse)

**Patrones clave:**
- **Embedding vs Referencing**: Datos que se leen juntos, se guardan juntos (embed); datos independientes con ciclo de vida propio, se referencian.
- **Bucket Pattern**: Agrupar documentos por período/unidad (ej. lecturas de sensor por hora en un solo documento).
- **Schema Versioning**: Campo `schema_version` para migrar documentos gradualmente.

### 2. Key-Value Stores (Redis, DynamoDB K/V, etcd, Hazelcast)

**Casos de uso ideales:**
- Caché de sesiones y datos calientes (Redis)
- Tokens de autenticación, rate limiting, contadores atómicos
- Configuración distribuida y service discovery (etcd, Consul)
- Leaderboards en tiempo real (Redis sorted sets)

**Cuándo NO usarlas:**
- Consultas por atributos que no son la clave primaria (sin índices secundarios)
- Datos que necesitan relaciones o agregaciones complejas
- Datos que no caben en memoria (Redis es in-memory por defecto)

### 3. Graph Databases (Neo4j, Neptune, Cosmos DB Gremlin, ArangoDB)

**Casos de uso ideales:**
- Redes sociales: seguidores, amistades, recomendaciones de contactos
- Motores de recomendación: "personas que compraron X también compraron Y"
- Grafos de conocimiento y ontologías empresariales
- Detección de fraude: patrones de transacciones entre entidades conectadas
- Gestión de dependencias: supply chain, infraestructura como código, bill of materials

**Cuándo NO usarlas:**
- Datos tabulares simples sin relaciones complejas entre entidades
- Reporting agregado tradicional (SQL es más eficiente)
- Cargas de escritura masivas (las DB de grafo optimizan lecturas de caminos)

### 4. Wide-Column Stores (Cassandra, ScyllaDB, HBase)

**Casos de uso ideales:**
- Escrituras masivas a alta velocidad: logs, telemetría IoT, eventos de clickstream
- Series temporales con alta cardinalidad: métricas por dispositivo/hora
- Datos geo-distribuidos: replicación multi-DC nativa en Cassandra
- Datos con patrón de acceso conocido (query-first design: modelas según las queries, no según las entidades)

**Cuándo NO usarlas:**
- Necesitas JOINs o agregaciones complejas ad-hoc
- Transacciones ACID multi-fila (Cassandra tiene LWT pero son costosas)
- El esquema de acceso cambia frecuentemente (rediseñar el modelo en Cassandra es costoso)

### 5. Search Engines (Elasticsearch, OpenSearch, Algolia, Meilisearch)

**Casos de uso ideales:**
- Búsqueda full-text con ranking de relevancia, facets y filtros
- Autocompletado y sugerencias de búsqueda (completion suggester)
- Análisis de logs con dashboards (ELK stack: Elasticsearch + Logstash + Kibana)
- Búsqueda geoespacial con scoring por proximidad
- Búsqueda vectorial/semántica (kNN en Elasticsearch 8.x+, OpenSearch 2.x+)

**Cuándo NO usarlas:**
- Como fuente primaria de verdad (no es ACID; usar como índice secundario de otra DB)
- Transacciones que requieren atomicidad entre documentos
- Almacenamiento de datos que no necesitan búsqueda textual

---

## Bases de Datos Multimodelo y Especializadas

### Multimodelo (Cosmos DB, ArangoDB, Couchbase)

Útiles cuando el mismo proyecto necesita múltiples paradigmas de acceso (documentos + grafos + key-value) y consolidar en un solo motor reduce la complejidad operativa. Pero **cuidado**: un solo motor no es mejor en todos los frentes — evalúa si la simplicidad operativa compensa la pérdida de features nativas de cada paradigma.

### Series Temporales (InfluxDB, TimescaleDB, Timestream, Prometheus)

**Indicadores para elegirlas:**
- Datos con timestamp como dimensión principal
- Consultas de ventana temporal (range queries, downsampling, retention policies)
- Alta tasa de ingesta de escritura con pocas actualizaciones

**TimescaleDB (PostgreSQL extension)** vs **InfluxDB**: TimescaleDB si ya usas PostgreSQL y necesitas SQL completo + JOINs con datos relacionales; InfluxDB si es puramente métricas/IoT y valoras el ecosistema Telegraf/Kapacitor.

### Ledger / Inmutables (Amazon QLDB, Azure Confidential Ledger)

Para datos que requieren **integridad criptográfica verificable** (contratos, registros financieros, cadena de custodia) — no es lo mismo que una DB con audit logging.

---

## Criterios de decisión ponderados

Al evaluar entre dos o más opciones, usa esta matriz con pesos según prioridades del proyecto:

| Criterio | Peso sugerido (total 100%) | Cómo evaluarlo |
|---|---|---|
| Consistencia de datos requerida (ACID vs BASE) | 20% | ¿Qué pasa si hay inconsistencia? ¿Dinero, salud, datos personales? |
| Escalabilidad necesaria (horizontal vs vertical) | 15% | ¿Volumen de datos y throughput esperado en 2 años? |
| Latencia objetivo (p95/p99 en ms) | 10% | ¿Usuarios interactivos o procesos batch nocturnos? |
| Complejidad de consultas esperadas | 15% | ¿JOINs, agregaciones, full-text, geospatial, grafos? |
| Experiencia del equipo | 15% | ¿El equipo ya opera PostgreSQL en producción? Eso vale más que la "mejor" DB teórica |
| Costo operativo (licencias, managed service, DevOps) | 10% | Self-hosted vs managed (RDS, Cosmos DB, Atlas) |
| Ecosistema y tooling (backups, migraciones, ORMs) | 10% | ¿Prisma/Django ORM lo soporta bien? ¿Hay terraform provider? |
| Cumplimiento (GDPR, residencia de datos, cifrado en reposo) | 5% | ¿La DB soporta TDE, CMK, VPC-only, audit logging? |

---

## Reglas de oro

1. **No uses una DB solo porque es nueva o "cool".** PostgreSQL resuelve el 80% de los casos reales mejor que una NoSQL mal aplicada.
2. **Una sola DB no es dogma.** Es válido tener PostgreSQL para datos transaccionales + Redis para caché + Elasticsearch para búsqueda — pero documenta por qué cada una y cómo se mantienen sincronizadas.
3. **El costo operativo real de una DB no es la licencia: es el equipo que la opera.** Dos DBs que el equipo conoce bien > una "mejor" DB que nadie sabe tunear ni hacer backup.
4. **Diseña para el patrón de acceso, no para la entidad.** En NoSQL, modelar según las queries (no según las tablas normalizadas) es fundamental — si el patrón de acceso no está claro, quédate con SQL hasta que lo esté.
5. **La DB correcta hoy puede no ser la correcta en 3 años.** Documenta en Supuestos/ADR por qué elegiste la DB actual y bajo qué condiciones se reconsideraría (ej. "si el volumen supera 10TB, migrar parte a Cassandra").

---

## Referencia rápida: servicios cloud por tipo de DB

| Tipo | AWS | Azure | GCP |
|---|---|---|---|
| **Relacional (OLTP)** | RDS (PostgreSQL, MySQL, MariaDB, Oracle, SQL Server), Aurora | Azure SQL Database, Azure DB for PostgreSQL/MySQL/MariaDB | Cloud SQL (PostgreSQL, MySQL, SQL Server) |
| **Relacional (distribuido)** | Aurora Global Database | Azure Cosmos DB for PostgreSQL (Citus) | Cloud Spanner, AlloyDB |
| **Document Store** | DocumentDB (MongoDB-compatible) | Azure Cosmos DB (SQL API, MongoDB API) | Firestore, MongoDB Atlas |
| **Key-Value** | DynamoDB, ElastiCache (Redis/Memcached) | Azure Cosmos DB (Table API), Azure Cache for Redis | Cloud Bigtable, Memorystore |
| **Graph** | Neptune | Cosmos DB Gremlin API | — (Neo4j Aura en marketplace) |
| **Wide-Column** | Keyspaces (Cassandra-compatible) | Cosmos DB Cassandra API | Cloud Bigtable |
| **Search** | OpenSearch Service | Azure Cognitive Search | Vertex AI Search |
| **Time-Series** | Timestream | Azure Data Explorer | BigQuery + partitioning |
| **Ledger** | QLDB | Azure Confidential Ledger | — |
