# Guía Senior: Backend Java / Spring Boot

Patrones, anti-patrones y convenciones para scaffolds de backend Java/Kotlin con Spring Boot. Aplica a proyectos greenfield y a módulos nuevos dentro de proyectos existentes.

---

## Estructura de proyecto (Clean/Hexagonal)

```
src/main/java/<base-package>/
├── domain/                          # Capa de dominio — SIN dependencias externas
│   ├── model/                       # Entidades de dominio (POJOs, no JPA entities)
│   │   ├── <Entidad>.java
│   │   ├── <Entidad>Id.java         # Value Object para IDs tipados
│   │   └── exception/               # DomainException, <Entidad>NotFoundException
│   ├── port/                        # Puertos (interfaces)
│   │   ├── inbound/                 # Casos de uso (UseCase interfaces)
│   │   │   └── Create<Entidad>UseCase.java
│   │   └── outbound/               # Repositorios, clientes externos
│   │       ├── <Entidad>Repository.java   # Interface en dominio
│   │       └── EventPublisher.java
│   └── service/                     # Implementaciones de casos de uso
│       └── Create<Entidad>Service.java
├── application/                     # Capa de aplicación (orquestación, DTOs)
│   ├── dto/                         # DTOs de entrada/salida (con validación Jakarta)
│   │   ├── Create<Entidad>Request.java
│   │   └── <Entidad>Response.java
│   └── mapper/                      # MapStruct interfaces (NO lógica manual)
│       └── <Entidad>Mapper.java
├── infrastructure/                  # Adaptadores (implementaciones de puertos outbound)
│   ├── persistence/                 # JPA entities, Spring Data repos, migraciones
│   │   ├── entity/                  # @Entity classes (separadas del domain model)
│   │   │   └── <Entidad>JpaEntity.java
│   │   ├── repository/             # Spring Data JPA Repository interfaces
│   │   │   └── <Entidad>JpaRepository.java
│   │   └── adapter/                # Implementación del puerto del dominio
│   │       └── <Entidad>RepositoryAdapter.java
│   ├── messaging/                   # Kafka/RabbitMQ/SQS productores y consumidores
│   └── client/                      # Clientes HTTP a servicios externos (Feign, RestClient)
└── presentation/                    # Controladores REST
    ├── controller/
    │   └── <Entidad>Controller.java
    └── advice/                      # @ControllerAdvice globales
        └── GlobalExceptionHandler.java
```

## Reglas de diseño senior

### 1. Domain Model != JPA Entity

**❌ Anti-patrón:** usar `@Entity` directamente en el modelo de dominio.

```java
// MAL: entidad JPA como modelo de dominio
@Entity
public class Order {
    @Id @GeneratedValue private Long id;
    // lógica de negocio mezclada con anotaciones JPA
}
```

**✅ Patrón correcto:** separar domain model (POJO puro) de persistence entity.

```java
// Domain model (sin anotaciones de infraestructura)
public class Order {
    private final OrderId id;
    private Money total;
    private OrderStatus status;

    // lógica de negocio pura, sin dependencias
    public void markAsShipped() {
        if (this.status != OrderStatus.PAID) {
            throw new OrderStateException("Solo órdenes pagadas pueden enviarse");
        }
        this.status = OrderStatus.SHIPPED;
    }
}

// JPA Entity (infrastructure)
@Entity
@Table(name = "orders")
class OrderJpaEntity {
    @Id @GeneratedValue private Long id;
    @Enumerated(EnumType.STRING) private String status;
    // ...
}

// Adapter que convierte
@Component
class OrderRepositoryAdapter implements OrderRepository {
    private final OrderJpaRepository jpaRepo;

    @Override
    public Optional<Order> findById(OrderId id) {
        return jpaRepo.findById(id.value()).map(this::toDomain);
    }
    private Order toDomain(OrderJpaEntity entity) { /* mapeo */ }
}
```

### 2. Value Objects para IDs y tipos primitivos

**✅ Siempre:** envolver IDs, emails, montos en Value Objects tipados. Previene bugs de pasar un `Long userId` donde va un `Long orderId`.

```java
public record OrderId(UUID value) {
    public OrderId {
        Objects.requireNonNull(value, "OrderId no puede ser null");
    }
}

public record Email(String value) {
    public Email {
        if (!value.matches("^[\\w-\\.]+@[\\w-]+\\.\\w{2,}$")) {
            throw new IllegalArgumentException("Email inválido: " + value);
        }
    }
}
```

### 3. MapStruct para mapeo, nunca manual

**✅ Siempre:** interfaces MapStruct declarativas. Jamás escribas `dto.setCampo(entity.getCampo())` a mano — es frágil, verboso y no escala.

```java
@Mapper(componentModel = "spring")
public interface OrderMapper {
    OrderResponse toResponse(Order domain);
    List<OrderResponse> toResponseList(List<Order> domains);

    @Mapping(target = "id", ignore = true)
    @Mapping(target = "status", constant = "PENDING")
    Order toDomain(CreateOrderRequest dto);
}
```

### 4. Manejo de errores centralizado

**✅ Siempre:** `@ControllerAdvice` global. Nunca try/catch en cada controller.

```java
@RestControllerAdvice
public class GlobalExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(OrderNotFoundException.class)
    ProblemDetail handleNotFound(OrderNotFoundException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(
            HttpStatus.NOT_FOUND, ex.getMessage());
        pd.setTitle("Orden no encontrada");
        pd.setProperty("timestamp", Instant.now());
        return pd;
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    ProblemDetail handleValidation(MethodArgumentNotValidException ex) {
        ProblemDetail pd = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        pd.setTitle("Error de validación");
        pd.setProperty("errors", ex.getBindingResult().getFieldErrors().stream()
            .map(fe -> Map.of("field", fe.getField(), "message", fe.getDefaultMessage()))
            .toList());
        return pd;
    }
}
```

### 5. Transacciones: @Transactional solo en casos de uso

**✅ Regla:** `@Transactional` va en la capa de aplicación/servicio (implementación del caso de uso), NUNCA en el controller ni en el repositorio. Un controller puede orquestar múltiples casos de uso; la transacción pertenece al caso de uso.

```java
@Service
@RequiredArgsConstructor
public class CreateOrderService implements CreateOrderUseCase {
    private final OrderRepository orderRepo;  // puerto de dominio
    private final EventPublisher publisher;

    @Override
    @Transactional
    public OrderResponse execute(CreateOrderRequest request) {
        Order order = Order.create(/* ... */);
        Order saved = orderRepo.save(order);
        publisher.publish(new OrderCreatedEvent(saved)); // si falla, rollback
        return orderMapper.toResponse(saved);
    }
}
```

### 6. Paginación estándar

```java
@GetMapping
public Page<OrderSummaryResponse> listOrders(
        @PageableDefault(size = 20, sort = "createdAt", direction = DESC) Pageable pageable,
        @RequestParam(required = false) OrderStatus status) {
    return orderService.findOrders(status, pageable)
        .map(orderMapper::toSummary);
}
```

### 7. Testing — reglas de oro

| Tipo | Framework | Convención |
|---|---|---|
| **Unitario (dominio)** | JUnit 5 + AssertJ | Nombre: `<Clase>Test`. Testea el modelo de dominio puro, sin Spring. Usa `@DisplayName` descriptivo en español o inglés consistente. |
| **Integración (repo)** | `@DataJpaTest` + Testcontainers | Nombre: `<Entidad>RepositoryIT`. PostgreSQL real en Testcontainers, no H2. |
| **Integración (API)** | `@WebMvcTest` o `@SpringBootTest(webEnvironment=RANDOM_PORT)` + MockMvc / WebTestClient | Nombre: `<Entidad>ControllerIT`. |
| **End-to-End** | Spring Boot Test + Testcontainers | Ejercicio completo de un flujo de negocio. Lo cubre `qa`, no `builder`. |

```java
@DisplayName("Order domain model")
class OrderTest {

    @Test
    @DisplayName("debe lanzar excepción al marcar como enviada una orden no pagada")
    void shouldThrowWhenShippingUnpaidOrder() {
        Order order = Order.create(/* ... */); // estado inicial PENDING
        assertThatThrownBy(order::markAsShipped)
            .isInstanceOf(OrderStateException.class)
            .hasMessageContaining("pagadas");
    }
}
```

### 8. Dockerfile para Spring Boot

```dockerfile
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY target/*.jar app.jar
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["java", "-XX:+UseZGC", "-jar", "app.jar"]
```

## Stack recomendado por defecto (greenfield)

| Rol | Tecnología | Alternativa |
|---|---|---|
| Lenguaje | Java 21 (LTS) | Kotlin 2.x |
| Build | Gradle (Kotlin DSL) | Maven |
| Framework | Spring Boot 3.x | Quarkus (si serverless/nativo) |
| ORM | Spring Data JPA + Hibernate 6 | jOOQ (si SQL complejo), R2DBC (si reactivo) |
| Migraciones | Flyway | Liquibase |
| Validación | Jakarta Bean Validation | — |
| Mapeo | MapStruct 1.6+ | — |
| Testing | JUnit 5 + AssertJ + Mockito | Kotest (Kotlin) |
| API Docs | Springdoc OpenAPI (Swagger UI) | — |
| Observabilidad | Micrometer + Actuator | OpenTelemetry Agent |
| Testcontainers | org.testcontainers:postgresql | — |
