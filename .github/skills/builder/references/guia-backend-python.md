# Guía Senior: Backend Python

Patrones, anti-patrones y convenciones para scaffolds de backend Python con FastAPI (recomendado), Django REST Framework y Flask.

---

## Estructura de proyecto (FastAPI + SQLAlchemy — Clean Architecture)

```
src/
├── domain/                          # Capa de dominio — sin dependencias de FastAPI ni DB
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── <entidad>.py             # Entidad de dominio (dataclass / Pydantic)
│   │   └── value_objects.py         # Value Objects (Email, Currency, etc.)
│   ├── ports/
│   │   ├── __init__.py
│   │   ├── repositories.py          # ABC / Protocol de repositorios
│   │   └── event_publisher.py       # Puerto de publicación de eventos
│   └── exceptions.py                # DomainException, NotFoundException
├── application/                     # Casos de uso (handlers de comandos/queries)
│   ├── __init__.py
│   ├── <entidad>/
│   │   ├── __init__.py
│   │   ├── commands.py              # Comandos (dataclass/pydantic inmutables)
│   │   ├── queries.py               # Queries (parámetros de búsqueda)
│   │   └── handlers.py              # Implementaciones de casos de uso
│   └── dto.py                       # DTOs de respuesta (Pydantic schemas)
├── infrastructure/                  # Adaptadores
│   ├── __init__.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── models.py                # SQLAlchemy ORM models (no confundir con domain models)
│   │   ├── repositories.py          # Implementación concreta de repositorios
│   │   ├── database.py              # async engine, session factory
│   │   └── alembic/                 # Migraciones Alembic
│   ├── clients/                     # httpx clients a servicios externos
│   └── messaging/                   # Productores/consumidores de eventos
├── presentation/                    # FastAPI routers
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py                  # Dependencias FastAPI (get_db, get_current_user)
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py            # Agrupa todos los routers v1
│   │       └── <entidad>/
│   │           ├── __init__.py
│   │           ├── router.py        # APIRouter con endpoints
│   │           └── schemas.py       # Pydantic schemas de request/response
│   └── middleware/
│       └── exception_handler.py     # Manejador global de excepciones
├── main.py                          # FastAPI app factory + lifespan
├── settings.py                      # pydantic-settings (BaseSettings)
└── pyproject.toml
```

## Reglas de diseño senior

### 1. Domain Model != SQLAlchemy Model (Clean Architecture)

**❌ Anti-patrón:** usar `Base = declarative_base()` como modelo de dominio.

```python
# MAL: SQLAlchemy model como dominio
class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID, primary_key=True)
    # lógica de negocio mezclada con ORM
```

**✅ Patrón correcto:**

```python
# domain/models/order.py — sin dependencias externas
from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Order:
    id: UUID
    customer_id: UUID
    status: OrderStatus = OrderStatus.PENDING
    items: list[OrderItem] = field(default_factory=list)

    def mark_as_paid(self) -> None:
        if self.status != OrderStatus.PENDING:
            raise DomainException("Solo órdenes pendientes pueden marcarse como pagadas")
        self.status = OrderStatus.PAID

# infrastructure/persistence/models.py — SQLAlchemy
class OrderModel(Base):
    __tablename__ = "orders"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    customer_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("customers.id"))
    status: Mapped[str] = mapped_column(String(20), default=OrderStatus.PENDING.value)

# infrastructure/persistence/repositories.py — adapter
class PostgresOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, order_id: UUID) -> Order | None:
        model = await self._session.get(OrderModel, order_id)
        return self._to_domain(model) if model else None

    def _to_domain(self, model: OrderModel) -> Order:
        return Order(id=model.id, customer_id=model.customer_id, ...)
```

### 2. FastAPI: Dependencias tipadas con Annotated (Python 3.10+)

**✅ Siempre:** usar `Annotated` para dependencias reutilizables.

```python
# presentation/api/deps.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncSession:
    async with async_session_factory() as session:
        yield session

DBSession = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]

# presentation/api/v1/orders/router.py
@router.post("/", response_model=OrderResponse, status_code=201)
async def create_order(
    body: CreateOrderRequest,
    db: DBSession,
    user: CurrentUser,
) -> OrderResponse:
    handler = CreateOrderHandler(PostgresOrderRepository(db))
    return await handler.execute(body, user.id)
```

### 3. Pydantic v2: model_config + field_validator

```python
from pydantic import BaseModel, Field, field_validator, ConfigDict

class CreateOrderRequest(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"  # Rechaza campos desconocidos
    )

    customer_id: uuid.UUID = Field(..., description="ID del cliente")
    items: list[OrderItemDto] = Field(..., min_length=1, max_length=50)
    notes: str | None = Field(default=None, max_length=500)

    @field_validator("items")
    @classmethod
    def validate_unique_products(cls, v: list[OrderItemDto]) -> list[OrderItemDto]:
        product_ids = [item.product_id for item in v]
        if len(product_ids) != len(set(product_ids)):
            raise ValueError("No puede haber productos duplicados en la orden")
        return v
```

### 4. Alembic + async SQLAlchemy

```python
# infrastructure/persistence/database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

engine = create_async_engine(
    str(settings.DATABASE_URL),  # postgresql+asyncpg://...
    echo=settings.DEBUG,
    pool_size=20,
    max_overflow=10,
)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)
```

**Configuración de Alembic (`alembic.ini` y `env.py`):**
- `env.py` debe usar el engine async con `run_async()`
- `target_metadata = Base.metadata` (importar desde `infrastructure.persistence.models`)

### 5. Manejador global de excepciones

```python
# presentation/middleware/exception_handler.py
from fastapi import Request
from fastapi.responses import JSONResponse

async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})

async def not_found_handler(request: Request, exc: NotFoundException) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})

# main.py — registrar en la app
app.add_exception_handler(DomainException, domain_exception_handler)
app.add_exception_handler(NotFoundException, not_found_handler)
```

### 6. Testing — reglas de oro

| Tipo | Framework | Convención |
|---|---|---|
| **Unitario (dominio)** | pytest + pytest-asyncio | Archivo: `test_<entidad>.py` en `tests/unit/`. Sin DB. |
| **Integración (repo)** | pytest + pytest-asyncio + Testcontainers (PostgreSQL en Docker) | `tests/integration/test_<entidad>_repository.py` |
| **API** | httpx.AsyncClient + pytest | `tests/api/test_<entidad>_routes.py`. Usar `app` fixture. |

```python
# tests/unit/test_order.py
async def test_mark_as_paid_changes_status():
    order = Order(id=uuid4(), customer_id=uuid4())
    order.mark_as_paid()
    assert order.status == OrderStatus.PAID

async def test_cannot_pay_shipped_order():
    order = Order(id=uuid4(), customer_id=uuid4())
    order.mark_as_paid()
    order.mark_as_shipped()
    with pytest.raises(DomainException, match="enviada"):
        order.mark_as_paid()  # No se puede pagar dos veces
```

### 7. Dockerfile para FastAPI

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync --frozen --no-dev
COPY src/ ./src/
EXPOSE 8000
HEALTHCHECK --interval=30s CMD python -c "import httpx; httpx.get('http://localhost:8000/health')"
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Stack recomendado por defecto (greenfield)

| Rol | Tecnología | Alternativa |
|---|---|---|
| Lenguaje | Python 3.12+ | — |
| Package Manager | uv (Astral) | Poetry |
| Framework | FastAPI | Django + DRF (si admin UI nativa), Litestar |
| ORM | SQLAlchemy 2.0 (async) | Django ORM (si Django), Tortoise ORM |
| Validación | Pydantic v2 | — |
| Migraciones | Alembic | — |
| Testing | pytest + pytest-asyncio + httpx | unittest (evitar) |
| API Docs | FastAPI built-in OpenAPI + Scalar | — |
| Async tasks | Celery + Redis / arq | Dramatiq, SAQ |
| Observabilidad | OpenTelemetry + structlog | — |
| Server | uvicorn (dev) / gunicorn + uvicorn workers (prod) | hypercorn |
