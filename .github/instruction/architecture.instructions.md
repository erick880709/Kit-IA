---
description: "Reglas de arquitectura limpia Bancolombia - estructura modular, capas, puertos y regla de dependencia"
applyTo: "**/*.{java,kt,sql,yml,yaml,properties,xml,gradle}"
---

# Bancolombia - Arquitectura Limpia (Clean Architecture)

Estas reglas son mandatorias para todos los proyectos del equipo. Se basan en el plugin oficial de Bancolombia
y los principios de Clean Architecture de Robert C. Martin.

Referencia oficial: https://bancolombia.github.io/scaffold-clean-architecture/docs/intro

---

## 1) Principios fundamentales

- Las dependencias siempre deben apuntar hacia adentro: las capas externas dependen de las internas, nunca al reves.
- El dominio no debe conocer ni depender de ninguna tecnologia de infraestructura (Spring, R2DBC, WebFlux, anotaciones de framework).
- Separacion estricta de responsabilidades entre capas: dominio, infraestructura y aplicacion.
- Los puertos (interfaces) se definen en el dominio; las implementaciones concretas van en infraestructura.

---

## 2) Estructura modular obligatoria

El proyecto es Gradle multimodular. La siguiente estructura es la referencia base:

```
NameProject
├── applications
│   └── app-service
│       ├── src/main/java/[package]
│       │   ├── config/             <- configuraciones de Spring y definicion de beans
│       │   └── MainApplication.java
│       ├── src/main/resources/
│       ├── src/test/java/[package]
│       └── build.gradle
├── deployment
│   └── [Dockerfile, Pipelines as a code]
├── domain
│   ├── model
│   │   ├── src/main/java/[package] <- modelos de dominio, entidades y puertos (interfaces)
│   │   ├── src/test/java/[package]
│   │   └── build.gradle
│   └── usecase
│       ├── src/main/java/[package] <- casos de uso y logica de aplicacion
│       ├── src/test/java/[package]
│       └── build.gradle
├── infrastructure
│   ├── driven-adapters             <- implementaciones concretas de puertos (BD, APIs externas)
│   ├── entry-points                <- REST controllers, consumers, inicio de flujos de negocio
│   └── helpers                    <- utilidades compartidas para driven-adapters y entry-points
├── .gitignore
├── build.gradle
├── gradle.properties
├── lombok.config
├── main.gradle
├── README.md
└── settings.gradle
```

---

## 3) Responsabilidades por capa

### 3.1 Domain - model

- Contiene los modelos de dominio y entidades: representacion de las reglas y logica de negocio.
- Define los puertos como interfaces Java que seran implementados en infraestructura.
- Sin dependencias de frameworks, Spring, R2DBC ni ninguna libreria de infraestructura.
- Sin anotaciones de Spring (`@Component`, `@Repository`, `@Service`, etc.).

### 3.2 Domain - usecase

- Contiene los casos de uso del sistema: define la logica de aplicacion.
- Reacciona a invocaciones desde los entry-points.
- Orquesta los flujos hacia el modelo de dominio usando exclusivamente los puertos definidos en `model`.
- Retorna siempre tipos reactivos: `Mono<T>` o `Flux<T>`.
- Unica dependencia permitida: modulo `model`. No puede depender de `infrastructure`.

### 3.3 Infrastructure - entry-points

- Contiene los puntos de entrada de la aplicacion: inicio de los flujos de negocio.
- Inicia los flujos delegando a los casos de uso. No contiene logica de negocio.
- Puede depender de `usecase` y `model`.
- No puede depender de `driven-adapters` ni `helpers`.

Tipos de entry-points disponibles via plugin (`gradle gep --type`):

| Tipo            | Descripcion                                      | Uso en el proyecto        |
|-----------------|--------------------------------------------------|---------------------------|
| `webflux`       | API REST reactiva con Spring WebFlux (Router/Handler) | Mandatorio para este stack |
| `restmvc`       | API REST con Spring MVC bloqueante               | No usar en servicios nuevos |
| `asynceventhandler` | Manejo de eventos asincrono (RabbitMQ/Kafka) | Segun necesidad del proyecto |
| `kafka`         | Consumer Kafka                                   | Segun necesidad del proyecto |
| `graphql`       | API GraphQL                                      | Segun necesidad del proyecto |
| `sqs`           | Listener SQS                                     | Segun necesidad del proyecto |

Estructura generada para `webflux`:

```
infrastructure/entry-points/reactive-web/
  src/main/java/[package]/
    api/
      Handler.java      <- maneja las peticiones HTTP, delega al UseCase
      RouterRest.java   <- define las rutas (router function)
  src/test/java/[package]/
    api/
      HandlerTest.java
      RouterRestTest.java
  build.gradle
```

Reglas de implementacion en `webflux`:
- Usar `RouterFunction` + `HandlerFunction`. No usar `@RestController` con metodos sincronos.
- El `Handler` recibe la `ServerRequest`, extrae parametros y delega al `UseCase`.
- El `RouterRest` solo define rutas. Sin logica de negocio.
- Metodos del Handler retornan siempre `Mono<ServerResponse>`.

### 3.4 Infrastructure - driven-adapters

- Implementaciones externas al sistema: conexiones a base de datos PostgreSQL, servicios REST, colas, archivos planos.
- Implementa los puertos (interfaces) definidos en `domain/model`.
- Puede depender de `model`. No puede depender de `usecase`.

Tipos de driven-adapters disponibles via plugin (`gradle gda --type`):

| Tipo             | Descripcion                                      | Uso en el proyecto          |
|------------------|--------------------------------------------------|-----------------------------|
| `r2dbc`          | Cliente R2DBC para PostgreSQL reactivo           | Mandatorio para persistencia |
| `restconsumer`   | Cliente REST consumidor (WebClient)              | Integraciones con APIs externas |
| `redis`          | Cache Redis (template o repository)              | Segun necesidad del proyecto |
| `asynceventbus`  | Bus de eventos asincrono (RabbitMQ/Kafka)        | Segun necesidad del proyecto |
| `secrets`        | Secrets Manager Bancolombia                      | Segun necesidad del proyecto |
| `jpa`            | Repositorio JPA                                  | No usar en servicios nuevos |

Reglas de implementacion en `r2dbc`:
- Usar `r2dbc` exclusivamente para persistencia con PostgreSQL. No usar `jpa`.
- El `Adapter` implementa la interfaz (puerto) definida en `domain/model`.
- Las entidades de persistencia (`@Table`) son exclusivas del modulo `driven-adapters`. No exponerlas al dominio.
- El mapeo entre entidad de persistencia y modelo de dominio se realiza en el `Adapter` mediante un mapper.
- Usar `R2dbcRepository` de Spring Data R2DBC para las operaciones CRUD reactivas.

Estructura generada para `r2dbc`:

```
infrastructure/driven-adapters/r2dbc-repository/
  src/main/java/[package]/
    r2dbc/
      config/
        PostgreSqlConnectionPool.java  <- configuracion del pool de conexiones
      helper/
        AdapterOperations.java         <- operaciones base del adaptador
      [Entity]R2dbcRepository.java     <- interfaz Spring Data R2DBC
      [Entity]RepositoryAdapter.java   <- implementacion del puerto de dominio
  src/test/java/[package]/
  build.gradle
```

### 3.5 Infrastructure - helpers

- Utilidades generales reutilizables por driven-adapters y entry-points.
- Sin logica de negocio.
- Las clases deben tener constructor privado y metodos estaticos unicamente.
- Todas las variables de clase deben ser `final`.

### 3.6 Application - app-service

- Modulo mas externo de la arquitectura.
- Responsable de ensamblar todos los modulos, resolver dependencias e inyectar instancias concretas.
- Unico modulo que contiene `public static void main(String[] args)`.
- Contiene configuraciones de Spring Boot y definicion de beans.

---

## 4) Reglas de dependencia entre modulos

| Modulo                          | Puede depender de              | No puede depender de                         |
|---------------------------------|-------------------------------|----------------------------------------------|
| domain/model                    | ninguno                       | usecase, infrastructure, applications        |
| domain/usecase                  | model                         | infrastructure, applications                 |
| infrastructure/entry-points     | usecase, model                | driven-adapters, helpers                     |
| infrastructure/driven-adapters  | model                         | usecase, entry-points                        |
| infrastructure/helpers          | model                         | usecase, entry-points, driven-adapters       |
| applications/app-service        | todos los modulos             | ninguno                                      |

---

## 5) Stack tecnologico obligatorio

- Java 17.
- Project Reactor: `Mono<T>` para respuestas de un elemento, `Flux<T>` para colecciones.
- Spring WebFlux para controladores reactivos. No usar controladores bloqueantes (`@RestController` con metodos sincronos).
- R2DBC para persistencia con PostgreSQL. No usar JPA ni Hibernate en servicios nuevos.
- Base de datos: PostgreSQL con esquema `schgrcap`.

---

## 6) Puertos (Ports) - convencion de definicion

Los puertos se definen como interfaces en `domain/model`. Las implementaciones concretas residen en `infrastructure/driven-adapters`.

```java
// En domain/model - definicion del puerto
public interface FinancialEffectGateway {
    Mono<FinancialEffect> findById(String effectId);
    Flux<FinancialEffect> findAll();
    Mono<FinancialEffect> save(FinancialEffect effect);
    Mono<Void> deleteById(String effectId);
}
```

```java
// En infrastructure/driven-adapters - implementacion concreta con R2DBC
@Repository
public class FinancialEffectAdapter implements FinancialEffectGateway {

    private final FinancialEffectR2dbcRepository repository;

    public FinancialEffectAdapter(FinancialEffectR2dbcRepository repository) {
        this.repository = repository;
    }

    @Override
    public Mono<FinancialEffect> findById(String effectId) {
        return repository.findByIdEfectoFinanciero(effectId)
                .map(FinancialEffectMapper::toDomain);
    }
}
```

---

## 7) Convencion de nombres por capa

| Capa                   | Sufijo recomendado          | Ejemplo                          |
|------------------------|-----------------------------|----------------------------------|
| domain/model           | sin sufijo tecnico          | `FinancialEffect`, `MacroEvent`  |
| domain/model (puerto)  | `Gateway`                   | `FinancialEffectGateway`         |
| domain/usecase         | `UseCase`                   | `RegisterFinancialEffectUseCase` |
| entry-points           | `Controller`, `Handler`     | `FinancialEffectController`      |
| driven-adapters        | `Adapter`, `Repository`     | `FinancialEffectAdapter`         |
| helpers                | sin sufijo tecnico          | `DateUtils`, `CurrencyConverter` |

No usar sufijos `DTO`, `Request`, `Response` en clases de dominio (`domain/model`).

---

## 8) Cuando falte informacion de arquitectura

Si una definicion estructural esta incompleta:
- Crear un `TODO` explicito con descripcion del requerimiento faltante.
- Formular 1-3 preguntas concretas para cerrar la definicion.
- No inventar ni asumir estructuras no definidas en este documento o en los documentos de referencia del equipo.
