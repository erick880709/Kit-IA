# Guía: Diseño de Esquemas de Base de Datos

Complementa a `guia-bases-de-datos.md` (selección de motor) con patrones de diseño de esquemas, migraciones y optimización para cada tipo de base de datos. Úsala durante la Sección 9 (Modelo de Datos) del documento de arquitectura y durante el scaffold de `builder`.

---

## Diseño de esquemas relacionales (SQL)

### Normalización vs Desnormalización

| Forma normal | Qué resuelve | Cuándo parar |
|---|---|---|
| **1NF** | Valores atómicos, sin listas en una celda | Siempre (mínimo indispensable) |
| **2NF** | Dependencia parcial de PK compuesta | Si tu PK es simple (UUID), 2NF ya se cumple |
| **3NF** | Dependencias transitivas (columna depende de otra no-PK) | **Parar aquí para OLTP**. Es el sweet spot. |
| **BCNF/4NF/5NF** | Anomalías de update en edge cases | Solo para sistemas financieros/regulatorios |

**Regla de oro para OLTP**: 3NF es suficiente. Normalizar más (BCNF+) es para sistemas donde un error de integridad cuesta plata real (bancos, contabilidad).

### Índices — reglas de diseño

```sql
-- 1. Todo FK debe tener índice (las migraciones de algunos ORMs no lo crean automático)
CREATE INDEX idx_orders_customer_id ON orders(customer_id);

-- 2. Índice compuesto: orden de columnas importa (filtro más selectivo primero)
CREATE INDEX idx_orders_status_created ON orders(status, created_at DESC);

-- 3. Partial index para queries con filtro constante
CREATE INDEX idx_active_orders ON orders(created_at) WHERE status = 'ACTIVE';

-- 4. Covering index (INCLUDE) para evitar lookup a la tabla
CREATE INDEX idx_orders_summary ON orders(customer_id) INCLUDE (status, total);
```

### Migraciones — estrategia

| Estrategia | Herramienta | Mejor para |
|---|---|---|
| **State-based** (declarativo) | Prisma, Atlas | Proyectos nuevos, schema como fuente de verdad |
| **Migration-based** (incremental) | Flyway, Alembic, EF Core Migrations | Proyectos existentes, control preciso de cada cambio |
| **Expand/Contract** | Manual + feature flags | Zero-downtime deploys, migraciones en producción |

### Particionado

```sql
-- Particionado por rango (fechas) — ideal para logs, eventos
CREATE TABLE events (
    id UUID DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL,
    payload JSONB
) PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_01 PARTITION OF events
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
```

---

## Diseño de esquemas NoSQL

### Document Store (MongoDB/DocumentDB/Cosmos DB SQL API)

**Patrones de modelado:**

| Patrón | Cuándo | Ejemplo |
|---|---|---|
| **Embedding** | Datos que se leen juntos, no cambian independientemente | Dirección de envío dentro de Orden |
| **Referencing** | Entidades con ciclo de vida propio, consultadas independientemente | `customer_id` en Orden → colección Customers |
| **Bucket** | Datos que crecen indefinidamente (time-series) | Lecturas de sensor agrupadas por hora en un doc |
| **Schema Versioning** | El schema evoluciona con el tiempo | Campo `schema_version: 2` en cada documento |

```javascript
// Ejemplo: Orden con Embedding (items) + Referencing (customer)
{
  _id: ObjectId("..."),
  customer_id: ObjectId("..."),  // referencia
  status: "PAID",
  items: [                       // embebido (se leen siempre con la orden)
    { product_id: "...", name: "Widget", qty: 2, price: 9.99 },
    { product_id: "...", name: "Gadget", qty: 1, price: 29.99 }
  ],
  shipping_address: {            // embebido (value object)
    street: "Av. Siempre Viva 742",
    city: "Springfield",
    zip: "12345"
  },
  schema_version: 1
}
```

### Graph DB (Neo4j/Neptune)

**Cuándo modelar como grafo y no como tablas:**

- La pregunta de negocio ES sobre las relaciones ("camino más corto entre X e Y", "personas que compraron X también compraron Y")
- La profundidad de la relación es variable (no sabés cuántos JOINs necesitás)
- El dominio es naturalmente un grafo (red social, supply chain, dependencias)

```cypher
// Modelo: (Usuario)-[COMPRO]->(Producto)
CREATE (u:Usuario {id: "U1", nombre: "Ana"})
CREATE (p:Producto {id: "P1", nombre: "Widget"})
CREATE (u)-[:COMPRO {fecha: date("2026-01-15"), cantidad: 2}]->(p)

// Query: ¿qué productos compraron quienes compraron lo mismo que Ana?
MATCH (ana:Usuario {id: "U1"})-[:COMPRO]->(p:Producto)<-[:COMPRO]-(otro:Usuario)-[:COMPRO]->(recomendado:Producto)
WHERE otro <> ana AND NOT (ana)-[:COMPRO]->(recomendado)
RETURN recomendado.nombre, count(*) AS frecuencia
ORDER BY frecuencia DESC LIMIT 5
```

---

## Patrones de acceso a datos (independiente del motor)

### Repository Pattern (Clean Architecture)

```python
# Puerto (dominio)
class OrderRepository(ABC):
    @abstractmethod
    async def find_by_id(self, order_id: UUID) -> Order | None: ...
    @abstractmethod
    async def save(self, order: Order) -> Order: ...

# Adaptador (infraestructura)
class PostgresOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def find_by_id(self, order_id: UUID) -> Order | None:
        result = await self._session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        model = result.scalar_one_or_none()
        return self._to_domain(model) if model else None
```

### Unit of Work Pattern

```python
class UnitOfWork(ABC):
    @abstractmethod
    async def commit(self) -> None: ...
    @abstractmethod
    async def rollback(self) -> None: ...

# Implementación con SQLAlchemy
class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
```

### CQRS a nivel de datos

```
[Command] → Write DB (PostgreSQL, normalizado) → [Evento] → Read DB (Elasticsearch/Redis/Materialized View, desnormalizado) → [Query]
```

La Write DB está optimizada para integridad transaccional. La Read DB está optimizada para el patrón de consulta específico del frontend/dashboard. Sincronización vía eventos o CDC.

---

## Checklist de diseño de datos (para `archi` Sección 9)

- [ ] ¿Cada entidad del dominio tiene un repositorio definido en el puerto?
- [ ] ¿Las relaciones FK tienen índices? (verificar en migraciones o schema)
- [ ] ¿El plan de migraciones está definido (Flyway/Alembic/Prisma/EF Core)?
- [ ] Si es SQL: ¿el esquema está en 3NF? ¿Hay desnormalización justificada?
- [ ] Si es Document Store: ¿embedded vs referencing está documentado?
- [ ] Si es Graph DB: ¿los tipos de relaciones están modelados explícitamente?
- [ ] ¿Soft deletes vs hard deletes está decidido?
- [ ] ¿Estrategia de backup/restore documentada?
- [ ] ¿Cifrado en reposo y en tránsito?
- [ ] ¿Conexiones desde la app usan pool + TLS + credenciales rotativas?
