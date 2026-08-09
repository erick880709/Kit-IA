---
description: "Reglas de implementacion backend Bancolombia - WebFlux, R2DBC, SonarQube, patrones y naming"
applyTo: "**/*.{java,kt,yml,yaml,properties,xml,gradle}"
---

# Bancolombia - Reglas de Implementacion Backend

Estas reglas son mandatorias para el desarrollo backend del equipo. Se aplican sobre el stack
Java 17 reactivo con Spring WebFlux, R2DBC y PostgreSQL, siguiendo la estructura definida en
`architecture.instructions.md`.

---

## 1) Spring WebFlux

### 1.1 Principios generales

- Todos los controladores son reactivos. No usar `@RestController` con metodos sincronos en servicios nuevos.
- Usar el modelo `RouterFunction` + `HandlerFunction`. No mezclar con `@GetMapping`, `@PostMapping` ni similares.
- Nunca bloquear el hilo reactivo: prohibido el uso de `.block()`, `.blockFirst()`, `.blockLast()` fuera de tests.
- No usar `Schedulers.boundedElastic()` como solucion a bloqueos. Resolver el bloqueo en la fuente.
- Propagar siempre el contexto reactivo. No usar variables de estado mutable compartidas entre operadores.

### 1.2 Estructura de un controlador WebFlux

```java
// RouterRest.java - solo define rutas, sin logica
@Configuration
public class RouterRest {

    @Bean
    public RouterFunction<ServerResponse> routerFunction(FinancialEffectHandler handler) {
        return RouterFunctions.route()
                .GET("/api/v1/financial-effects/{id}", handler::findById)
                .POST("/api/v1/financial-effects", handler::save)
                .DELETE("/api/v1/financial-effects/{id}", handler::deleteById)
                .build();
    }
}

// Handler.java - recibe peticion, delega al UseCase, construye respuesta
@Component
public class FinancialEffectHandler {

    private final RegisterFinancialEffectUseCase registerUseCase;
    private final FindFinancialEffectUseCase findUseCase;

    public FinancialEffectHandler(RegisterFinancialEffectUseCase registerUseCase,
                                   FindFinancialEffectUseCase findUseCase) {
        this.registerUseCase = registerUseCase;
        this.findUseCase = findUseCase;
    }

    public Mono<ServerResponse> findById(ServerRequest request) {
        var effectId = request.pathVariable("id");
        return findUseCase.findById(effectId)
                .flatMap(effect -> ServerResponse.ok().bodyValue(effect))
                .switchIfEmpty(ServerResponse.notFound().build());
    }

    public Mono<ServerResponse> save(ServerRequest request) {
        return request.bodyToMono(FinancialEffect.class)
                .flatMap(registerUseCase::execute)
                .flatMap(saved -> ServerResponse.status(HttpStatus.CREATED).bodyValue(saved));
    }
}
```

### 1.3 Manejo de errores reactivo

- Usar `onErrorMap` para transformar excepciones tecnicas en excepciones de dominio.
- Usar `onErrorResume` para retornar valores alternativos en flujos controlados.
- Centralizar el manejo de errores HTTP en un `@Component` que implemente `WebExceptionHandler`.
- No lanzar excepciones en medio de cadenas reactivas con `throw`. Usar `Mono.error(new ...)`.

```java
// Correcto
return gateway.findById(id)
        .switchIfEmpty(Mono.error(new EntityNotFoundException("Efecto no encontrado: " + id)))
        .onErrorMap(DataAccessException.class, ex -> new RepositoryException("Error de acceso a datos", ex));

// Incorrecto
return gateway.findById(id)
        .map(effect -> {
            if (effect == null) throw new RuntimeException("no encontrado"); // prohibido
            return effect;
        });
```

### 1.4 Reglas de operadores Reactor

- Usar `flatMap` para operaciones asincronas que retornan `Mono`/`Flux`.
- Usar `map` solo para transformaciones sincronas.
- Usar `zipWith` o `zip` para combinar dos fuentes independientes.
- Usar `concatMap` cuando el orden de ejecucion secuencial es requerido.
- Preferir `switchIfEmpty` sobre `defaultIfEmpty` cuando se requiere logica adicional.

---

## 2) R2DBC con PostgreSQL

### 2.1 Principios generales

- Usar R2DBC exclusivamente para persistencia. Prohibido JPA e Hibernate en servicios nuevos.
- Las entidades de persistencia (`@Table`) residen unicamente en `infrastructure/driven-adapters`.
- El modelo de dominio no tiene anotaciones de persistencia (`@Table`, `@Column`, `@Id` de Spring Data).
- El mapeo entre entidad de persistencia y modelo de dominio es responsabilidad del `Adapter`.

### 2.2 Definicion de entidad R2DBC

```java
// En infrastructure/driven-adapters - entidad de persistencia
@Table("schgrcap.efecto_financiero")
public class FinancialEffectEntity {

    @Id
    private Long id;

    @Column("id_efecto_financiero")
    private String financialEffectId;

    @Column("id_evento_materializado")
    private String materializedEventId;

    @Column("valor_cop")
    private BigDecimal valueCop;

    @Column("valor_usd")
    private BigDecimal valueUsd;

    @Column("fecha_creacion")
    private OffsetDateTime creationDate;
}
```

### 2.3 Definicion de repositorio R2DBC

```java
// Interfaz Spring Data R2DBC - solo en driven-adapters
public interface FinancialEffectR2dbcRepository extends ReactiveCrudRepository<FinancialEffectEntity, Long> {

    Mono<FinancialEffectEntity> findByFinancialEffectId(String financialEffectId);

    @Query("SELECT * FROM schgrcap.efecto_financiero WHERE id_evento_materializado = :eventId")
    Flux<FinancialEffectEntity> findAllByMaterializedEventId(String eventId);
}
```

### 2.4 Implementacion del Adapter

```java
// Implementa el puerto de dominio, realiza el mapeo entidad <-> modelo
@Repository
public class FinancialEffectAdapter implements FinancialEffectGateway {

    private final FinancialEffectR2dbcRepository repository;

    public FinancialEffectAdapter(FinancialEffectR2dbcRepository repository) {
        this.repository = repository;
    }

    @Override
    public Mono<FinancialEffect> findById(String effectId) {
        return repository.findByFinancialEffectId(effectId)
                .map(FinancialEffectMapper::toDomain);
    }

    @Override
    public Mono<FinancialEffect> save(FinancialEffect effect) {
        return Mono.just(effect)
                .map(FinancialEffectMapper::toEntity)
                .flatMap(repository::save)
                .map(FinancialEffectMapper::toDomain);
    }
}
```

### 2.5 Configuracion de conexion

- Usar `application.yml` para la configuracion de la conexion R2DBC. No hardcodear credenciales.
- El esquema por defecto del proyecto es `schgrcap`.
- Las queries SQL largas (mas de 120 caracteres) deben dividirse en multiples lineas.

```yaml
spring:
  r2dbc:
    url: r2dbc:postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    properties:
      schema: schgrcap
```

### 2.6 Queries nativas con `@Query`

- Nombrar parametros con `:nombre` (no con `?` posicional).
- Dividir queries largas en multiples lineas usando concatenacion o bloques de texto.
- Incluir el esquema en el nombre de tabla: `schgrcap.nombre_tabla`.

---

## 3) Reglas SonarQube

### 3.1 Critico (bloquean el merge)

- **S5411 - Boolean wrapper**: usar `Boolean.TRUE` / `Boolean.FALSE`, no literales `true` / `false` en constructores y metodos que esperan `Boolean`.
- **SCAFFOLD - @Configuration**: no declarar campos `@Value` en clases `@Configuration`. Inyectar el valor directamente en el parametro del metodo `@Bean`.

```java
// Incorrecto
@Configuration
public class TimeoutConfig {
    @Value("${service.timeout}") private int timeout;
    @Bean public ServiceClient client() { return new ServiceClient(timeout); }
}

// Correcto
@Configuration
public class TimeoutConfig {
    @Bean
    public ServiceClient client(@Value("${service.timeout}") int timeout) {
        return new ServiceClient(timeout);
    }
}
```

### 3.2 Alto (deuda tecnica, deben resolverse en el sprint)

- **S107 - Maximo 4 parametros por metodo**: usar Records para agrupar parametros relacionados.
- **S1200 - Maximo 20 dependencias por clase**: dividir en servicios especializados.
- **S138 - Maximo 30 lineas por metodo**: extraer metodos privados con nombre descriptivo.
- **S109 - Sin numeros magicos**: extraer a constantes `UPPER_SNAKE_CASE` de menos de 40 caracteres.
- **S1192 - Strings duplicados (3 o mas veces)**: extraer a constante privada.
- **S3776 - Complejidad cognitiva alta**: aplicar early returns y extraer metodos.
- **S1940 - Boolean wrapper en negacion**: usar `Boolean.FALSE.equals(valor)` en lugar de `!valor`.

```java
// S107 - Incorrecto: 6 parametros
public Flux<Item> findItems(String id, String name, Integer offset,
                             Integer limit, String sort, String order) { }

// S107 - Correcto: Records agrupan parametros
public record SearchFilters(String id, String name) {}
public record PaginationParams(Integer offset, Integer limit) {
    private static final int DEFAULT_PAGE_SIZE = 10;
    private static final int DEFAULT_OFFSET = 0;
    public int safeOffset() { return offset == null ? DEFAULT_OFFSET : offset; }
    public int safeLimit() { return limit == null ? DEFAULT_PAGE_SIZE : limit; }
}

public Flux<Item> findItems(SearchFilters filters, PaginationParams pagination) { }
```

### 3.3 Medio (legibilidad, deben resolverse antes de cierre del sprint)

- **S6212 - Usar `var`**: cuando el tipo es obvio por el contexto (no usar con tipos reactivos `Mono`/`Flux`).
- **S1941 - Variables cerca de uso**: declarar la variable justo antes de usarla.
- **S1611 - Lambdas sin llaves**: una sola expresion no necesita `{ return ...; }`.
- **S1612 - Method references**: preferir `.map(User::getName)` sobre `.map(u -> u.getName())`.
- **S103 - Maximo 120 caracteres por linea**.
- **S1120 - Indentacion**: 4 espacios por nivel. No usar tabuladores.
- **S139 - Sin comentarios al final de linea (trailing comments)**: el comentario va en linea separada.
- **S1858 - Sin sufijos tecnicos en dominio**: eliminar DTO, Request, Response de clases en `domain/model`.

### 3.4 Bajo (limpieza y consistencia)

- **S6068 - Sin `eq()` redundante en Mockito**: usar valores directos; `eq()` solo cuando se combina con `any()`.
- **S1128 - Sin imports no usados**.
- **S1854 / S1481 - Sin variables no usadas**: eliminar codigo muerto.
- **S1118 - Utility classes**: constructor privado que lanza `IllegalStateException`.
- **S112 - Excepciones especificas**: no lanzar `RuntimeException` generica.
- **S1144 - Sin metodos privados no usados**.
- **S864 - Parentesis explicitos**: clarificar expresiones con `&&` y `||`.
- **S120 - Packages en minusculas**: `^[a-z_]+(\\.[a-z_][a-z0-9_]*)*$`.
- **S1602 - Lambdas sin llaves**: una expresion de una linea no necesita `{ }`.
- **S2094 - Constructores vacios**: documentar con comentario por que existe el constructor vacio.

---

## 4) Patrones de diseño

Los siguientes patrones son los permitidos y recomendados para este proyecto.

### 4.1 Factory

Usar cuando la creacion de un objeto requiere logica condicional o es compleja.
La fabrica reside en `domain/model` si crea objetos de dominio, o en `driven-adapters` si crea entidades de infraestructura.

```java
public class FinancialEffectFactory {

    private FinancialEffectFactory() {
        throw new IllegalStateException("Utility class");
    }

    public static FinancialEffect createFromEvent(MaterializedEvent event, BigDecimal valueCop) {
        return FinancialEffect.builder()
                .financialEffectId(UUID.randomUUID().toString())
                .materializedEventId(event.getId())
                .valueCop(valueCop)
                .creationDate(LocalDateTime.now())
                .build();
    }
}
```

### 4.2 Strategy

Usar cuando existen multiples algoritmos o comportamientos intercambiables para una misma operacion.
La interfaz de estrategia reside en `domain/model`; las implementaciones en `usecase` o `driven-adapters` segun corresponda.

```java
// Interfaz de estrategia en domain/model
public interface CurrencyConversionStrategy {
    Mono<BigDecimal> convert(BigDecimal amount, String sourceCurrency, String targetCurrency);
}

// Implementacion en driven-adapters
@Component("tcrmConversion")
public class TcrmCurrencyConversionAdapter implements CurrencyConversionStrategy {
    @Override
    public Mono<BigDecimal> convert(BigDecimal amount, String sourceCurrency, String targetCurrency) {
        // implementacion con cliente externo
    }
}
```

### 4.3 Builder

Usar para construir objetos de dominio con muchos campos opcionales.
Preferir Lombok `@Builder` en clases de dominio cuando el numero de campos supera 4.

```java
@Builder
public class FinancialEffect {
    private final String financialEffectId;
    private final String materializedEventId;
    private final BigDecimal valueCop;
    private final BigDecimal valueUsd;
    private final String currency;
    private final LocalDateTime creationDate;
}
```

### 4.4 Domain Service

Usar para logica de negocio que no pertenece naturalmente a una entidad de dominio especifica
y que opera sobre multiples entidades o requiere coordinacion entre puertos.
Reside en `domain/usecase`.

```java
// En domain/usecase
public class FinancialEffectValidationService {

    public Mono<FinancialEffect> validateAndEnrich(FinancialEffect effect,
                                                    MaterializedEvent event) {
        return validateCurrency(effect)
                .flatMap(valid -> validateBusinessLine(valid, event))
                .map(this::enrichWithDefaults);
    }

    private Mono<FinancialEffect> validateCurrency(FinancialEffect effect) {
        if (effect.getCurrency() == null || effect.getCurrency().isBlank()) {
            return Mono.error(new InvalidEffectException("La divisa es obligatoria"));
        }
        return Mono.just(effect);
    }
}
```

---

## 5) Convenciones de naming

### 5.1 General

- Codigo en **ingles**. Comentarios, logs y mensajes de error en **espanol**.
- Clases y paquetes en `UpperCamelCase`.
- Variables y metodos en `lowerCamelCase`. Minimo 3 caracteres: `^[a-z][a-zA-Z0-9]{2,}$`.
- Constantes en `UPPER_SNAKE_CASE` de menos de 40 caracteres.
- Paquetes en minusculas con separador punto: `^[a-z_]+(\\.[a-z_][a-z0-9_]*)*$`.

### 5.2 Clases por capa

| Capa                        | Patron de nombre              | Ejemplo                            |
|-----------------------------|-------------------------------|------------------------------------|
| `domain/model` - entidad    | Sustantivo sin sufijo tecnico | `FinancialEffect`, `MacroEvent`    |
| `domain/model` - puerto     | Sustantivo + `Gateway`        | `FinancialEffectGateway`           |
| `domain/usecase`            | Verbo/sustantivo + `UseCase`  | `RegisterFinancialEffectUseCase`   |
| `entry-points` - router     | Entidad + `RouterRest`        | `FinancialEffectRouterRest`        |
| `entry-points` - handler    | Entidad + `Handler`           | `FinancialEffectHandler`           |
| `driven-adapters` - adapter | Entidad + `Adapter`           | `FinancialEffectAdapter`           |
| `driven-adapters` - repo    | Entidad + `R2dbcRepository`   | `FinancialEffectR2dbcRepository`   |
| `helpers`                   | Sustantivo + sufijo funcional | `DateUtils`, `CurrencyConverter`   |
| `@Configuration`            | Dominio + `Config`            | `DatabaseConfig`, `SecurityConfig` |

### 5.3 Prohibiciones de naming

- No usar sufijos `DTO`, `Request`, `Response` en clases de `domain/model`.
- No usar el nombre de la tecnologia en clases de dominio: `JpaEffect`, `R2dbcEvent`.
- No nombrar paquetes con mayusculas: `co.com.bancolombia.FinancialEffect` es incorrecto.
- Los metodos no pueden tener menos de 3 caracteres. Excepcion: `id()`, `of()`, `to()` en Records o factories estaticas.

### 5.4 Tests

- Nombre del metodo en ingles, conciso, maximo 50 caracteres: `testSaveNewEffect`, `testFindByIdNotFound`.
- Usar `@DisplayName` en espanol para la descripcion completa del escenario.
- Patron de nombre: `test + Accion + Condicion`.

```java
@Test
@DisplayName("Retorna efecto financiero cuando el ID existe")
void testFindByIdExisting() { }

@Test
@DisplayName("Retorna vacio cuando el ID no existe")
void testFindByIdNotFound() { }
```

### 5.5 Constantes

- Definir en la clase que las usa, o en una clase de utilidad con constructor privado si son compartidas.
- Maximo 40 caracteres en el nombre.
- No usar numeros magicos en logica de negocio.

```java
// Correcto
private static final int DEFAULT_PAGE_SIZE = 10;
private static final String PARAM_ESTADO = "estado";
private static final String SCHEMA_PREFIX = "schgrcap.";

// Incorrecto
if (size <= 0 ? 10 : size) { }        // numero magico
.bind("estado", value)                // string duplicado 3+ veces sin constante
```

---

## 6) Buenas practicas para tests

### 6.1 Regla de oro del refactoring

Al refactorizar codigo, los tests DEBEN seguir pasando sin modificaciones.
Si se modifican los tests durante un refactoring, se esta cambiando logica de negocio, no haciendo refactoring.

### 6.2 Tests reactivos con StepVerifier

Todo codigo que retorne `Mono` o `Flux` debe validarse con `StepVerifier`. No usar `.block()` en tests.

Estructura recomendada:

```java
@Test
@DisplayName("Retorna el efecto financiero cuando el ID existe")
void shouldReturnEffectWhenIdExists() {
    // Preparacion de datos
    var entity = createFinancialEffectEntity();
    when(repository.findByFinancialEffectId(EFFECT_ID))
            .thenReturn(Mono.just(entity));

    // Ejecucion
    var result = adapter.findById(EFFECT_ID);

    // Validacion con StepVerifier
    StepVerifier.create(result)
            .assertNext(effect -> assertThat(effect.getFinancialEffectId()).isEqualTo(EFFECT_ID))
            .verifyComplete();

    // Verificacion de interacciones
    verify(repository).findByFinancialEffectId(EFFECT_ID);
}
```

Elementos obligatorios en cada test:
- `@DisplayName` en espanol con descripcion completa del escenario.
- Comentarios en espanol indicando cada fase: preparacion, ejecucion, validacion.
- Constantes para todos los valores usados en el test.
- `StepVerifier` para validar `Mono`/`Flux`.
- `verify()` para confirmar interacciones con mocks.
- Metodo helper privado para construir datos de prueba.

### 6.3 Metodo helper para datos de prueba

No repetir la construccion de objetos en cada test. Usar un metodo helper privado reutilizable.

```java
// Incorrecto: construccion repetida en cada test
@Test
void testFindById() {
    var entity = new FinancialEffectEntity();
    entity.setId(1L);
    entity.setFinancialEffectId("EF-001");
    entity.setValueCop(BigDecimal.TEN);
}

// Correcto: metodo helper reutilizable
private static final String EFFECT_ID = "EF-001";
private static final BigDecimal VALUE_COP = BigDecimal.TEN;

private FinancialEffectEntity createFinancialEffectEntity() {
    var entity = new FinancialEffectEntity();
    entity.setId(1L);
    entity.setFinancialEffectId(EFFECT_ID);
    entity.setValueCop(VALUE_COP);
    return entity;
}
```

### 6.4 Nombres de tests

Dos patrones validos, usar de forma consistente dentro del mismo archivo:

| Patron           | Ejemplo                              | Cuando usarlo             |
|------------------|--------------------------------------|---------------------------|
| `test+Accion+Condicion` | `testFindByIdNotFound`      | Tests concisos y directos |
| `should+Accion+When+Condicion` | `shouldReturnEmptyWhenIdNotFound` | Tests con escenario complejo |

Reglas adicionales:
- Nombre del metodo en ingles, maximo 50 caracteres.
- `@DisplayName` en espanol con descripcion completa.
- No usar `snake_case` ni mayusculas iniciales: `Test_Save_Element` es incorrecto.
- No usar nombres genericos: `test1`, `testSave`, `testMethod`.

### 6.5 Reglas especificas de SonarQube en tests

- No usar `var` con tipos reactivos en tests: el tipo debe ser explicito para mayor claridad.
- Dividir aserciones `StepVerifier` en multiples lineas si superan 120 caracteres.
- `Boolean.TRUE` / `Boolean.FALSE` aplica tambien en la preparacion de mocks.

```java
// Incorrecto: var con tipo reactivo no obvio
var count = repository.count();

// Correcto: tipo explicito
Mono<Long> count = repository.count();

// Incorrecto: StepVerifier en una sola linea > 120 chars
StepVerifier.create(result).assertNext(r -> assertThat(r.getValueCop()).isEqualTo(VALUE_COP)).verifyComplete();

// Correcto: dividido en multiples lineas
StepVerifier.create(result)
        .assertNext(r -> assertThat(r.getValueCop()).isEqualTo(VALUE_COP))
        .verifyComplete();
```

---

## 7) Limite de complejidad

| Regla                          | Limite  | Fuente               | Accion si se supera                 |
|--------------------------------|---------|----------------------|-------------------------------------|
| Parametros por metodo          | 4       | Guia estilo / S107   | Agrupar en Records                  |
| Dependencias por clase         | 20      | S1200 (mas restrictivo que guia: 22) | Dividir en servicios especializados |
| Lineas por metodo              | 30      | Guia estilo / S138   | Extraer metodos privados            |
| Campos por clase               | 30      | Guia estilo          | Dividir responsabilidades           |
| Caracteres por linea           | 120     | Guia estilo / S103   | Dividir en multiples lineas         |
| Complejidad cognitiva          | baja    | S3776                | Early returns, extraer metodos      |

---

## 7) Cuando falte informacion de implementacion

Si una definicion tecnica esta incompleta:
- Crear un `TODO` explicito con descripcion del requerimiento faltante.
- Formular 1-3 preguntas concretas para cerrar la definicion.
- No inventar ni asumir valores de configuracion, limites de negocio ni comportamientos no documentados.
