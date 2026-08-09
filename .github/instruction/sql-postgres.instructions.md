---
description: "Reglas de persistencia Bancolombia - PostgreSQL, R2DBC, convenciones DDL y mapeo Java"
applyTo: "**/*.{sql,java,kt,yml,yaml,properties}"
---

# Bancolombia - Persistencia con PostgreSQL y R2DBC

Estas reglas aplican a todo el codigo de acceso a datos del proyecto. Las convenciones de nomenclatura,
tipado y estructura son mandatorias. Los ejemplos de codigo usan el esquema `schgrcap` y las tablas
`efecto_financiero`, `evento_materializado` y `recuperacion` como referencia ilustrativa.

El esquema, las tablas y las columnas concretas varian por proyecto. Siempre basar la implementacion
en los DDLs oficiales del proyecto en curso, no en los ejemplos de este documento.

---

## 1) Esquema y base de datos

- El esquema de trabajo lo define el proyecto. Toda referencia a tablas debe incluirlo: `schema.nombre_tabla`.
- No crear tablas ni columnas fuera del esquema definido para el proyecto sin aprobacion de arquitectura.
- La base de datos es **PostgreSQL**. No usar sintaxis ni funciones exclusivas de otros motores.
- Las credenciales de conexion se inyectan por variables de entorno. No hardcodear valores.

```yaml
# application.yml - configuracion minima obligatoria
# Reemplazar los valores de ejemplo con los del proyecto en curso
spring:
  r2dbc:
    url: r2dbc:postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    properties:
      schema: ${DB_SCHEMA}       # ejemplo: schgrcap
  sql:
    init:
      schema-locations: classpath:schema.sql
```

---

## 2) Convenciones de nomenclatura en DDL

### 2.1 Tablas

- Nombres en `snake_case`, en espanol, en plural o sustantivo segun el dominio.
- Las tablas maestras (catalogos) llevan el prefijo `m_`: `m_canal`, `m_linea_negocio`, `m_consecuencia`.
- Las tablas de relacion (N:M) llevan el prefijo `rx_`: `rx_riesgo_efecto`, `rx_efecto_programa`.

| Tipo de tabla   | Convencion       | Ejemplo                        |
|-----------------|------------------|--------------------------------|
| Transaccional   | `snake_case`     | `efecto_financiero`, `recuperacion` |
| Maestra         | `m_` + nombre    | `m_canal`, `m_producto`        |
| Relacion N:M    | `rx_` + entidades | `rx_riesgo_efecto`            |

### 2.2 Columnas

- Nombres en `snake_case`, en espanol.
- Las columnas ID de negocio (no el PK tecnico) llevan el prefijo `id_`: `id_efecto_financiero`, `id_recuperacion`.
- Las columnas FK hacia otras tablas llevan el prefijo `id_`: `id_evento_materializado`, `id_compania_contable`.
- Las columnas de auditoria son obligatorias en todas las tablas transaccionales (ver seccion 2.4).

### 2.3 Constraints

| Tipo          | Patron de nombre                          | Ejemplo                                         |
|---------------|-------------------------------------------|-------------------------------------------------|
| Primary key   | `pk_nombre_tabla`                         | `pk_efecto_financiero`                          |
| Foreign key   | `fk_tabla_origen_columna`                 | `fk_recuperacion_cc`, `fk_canal_compania`       |
| Unique        | `nombre_tabla_un` o `unique_descripcion`  | `efecto_financiero_un`, `recuperacion_un`       |
| Check         | `chk_descripcion`                         | `chk_idriesgo_desencadenado_recibido`           |
| Index         | `tabla_columna_idx` o `idx_descripcion`   | `efecto_financiero_id_canal_idx`                |

### 2.4 Columnas de auditoria obligatorias

Toda tabla transaccional debe incluir las siguientes columnas de auditoria:

```sql
fecha_creacion  timestamptz NOT NULL DEFAULT now(),
fecha_modificacion timestamptz NULL,
id_usuario_creador int4 NOT NULL,
id_usuario_modificador int4 NULL
```

---

## 3) Tipos de datos PostgreSQL y su mapeo a Java

Usar la siguiente tabla como referencia obligatoria al crear entidades R2DBC:

| Tipo PostgreSQL        | Tipo Java          | Ejemplo de columna                        |
|------------------------|--------------------|-------------------------------------------|
| `bigserial`            | `Long`             | `id bigserial NOT NULL` (PK tecnico)      |
| `serial4`              | `Integer`          | `id_evento serial4 NOT NULL`              |
| `int2`                 | `Short`            | `id_compania_contable int2`               |
| `int4`                 | `Integer`          | `id_geografia int4`                       |
| `int8`                 | `Long`             | `id_plan_accion int8`                     |
| `varchar(n)`           | `String`           | `id_efecto_financiero varchar(100)`       |
| `text`                 | `String`           | `descripcion text`                        |
| `numeric(18, 6)`       | `BigDecimal`       | `valor_cop numeric(18, 6)`                |
| `numeric(21, 6)`       | `BigDecimal`       | `valor_divisa_origen numeric(21, 6)`      |
| `timestamptz`          | `OffsetDateTime`   | `fecha_creacion timestamptz`              |
| `timestamp`            | `LocalDateTime`    | `fecha_contable timestamp`                |
| `bool`                 | `Boolean`          | `afecto_consumidor bool`                  |
| `date`                 | `LocalDate`        | `fecha_inicio_operacion date`             |

Reglas adicionales de mapeo:
- No usar `java.util.Date` ni `java.sql.Timestamp`. Usar siempre tipos de `java.time`.
- Las columnas `timestamptz` se mapean a `OffsetDateTime`. Las columnas `timestamp` a `LocalDateTime`.
- Las columnas `numeric` de valores monetarios se mapean a `BigDecimal`. No usar `double` ni `float`.
- Los campos `bool` de PostgreSQL se mapean a `Boolean` (wrapper, no primitivo), para respetar nulabilidad.

---

## 4) Definicion de entidades R2DBC

### 4.1 Estructura de la entidad

```java
// En infrastructure/driven-adapters/r2dbc-repository
@Table("schgrcap.efecto_financiero")
public class FinancialEffectEntity {

    @Id
    private Long id;

    @Column("id_efecto_financiero")
    private String financialEffectId;

    @Column("id_evento_materializado")
    private String materializedEventId;

    @Column("divisa_origen")
    private String sourceCurrency;

    @Column("valor_cop")
    private BigDecimal valueCop;

    @Column("valor_usd")
    private BigDecimal valueUsd;

    @Column("valor_divisa_origen")
    private BigDecimal valueSourceCurrency;

    @Column("fecha_contable")
    private LocalDateTime accountingDate;

    @Column("fecha_creacion")
    private OffsetDateTime creationDate;

    @Column("fecha_modificacion")
    private OffsetDateTime modificationDate;

    @Column("id_usuario_creador")
    private Integer creatorUserId;

    @Column("id_usuario_modificador")
    private Integer modifierUserId;
}
```

### 4.2 Reglas de las entidades

- La anotacion `@Table` siempre incluye el esquema: `@Table("schgrcap.nombre_tabla")`.
- La anotacion `@Column` es obligatoria cuando el nombre del campo Java no coincide exactamente con la columna en base de datos.
- El campo anotado con `@Id` corresponde al PK tecnico autoincremental (`bigserial`, `serial4`).
- Las entidades no tienen logica de negocio. Solo getters, setters y anotaciones de persistencia.
- No usar Lombok `@Data` en entidades R2DBC: puede generar problemas con el proxy reactivo. Usar `@Getter` y `@Setter` de forma explicita.

### 4.3 Relaciones entre entidades

R2DBC no soporta `@OneToMany` ni `@ManyToOne` automaticos. Las relaciones se resuelven en el `Adapter` mediante queries separadas y composicion reactiva.

```java
// Correcto: relacion resuelta en el Adapter con operadores reactivos
public Mono<FinancialEffect> findByIdWithEvent(String effectId) {
    return repository.findByFinancialEffectId(effectId)
            .flatMap(entity -> eventRepository.findByMaterializedEventId(entity.getMaterializedEventId())
                    .map(eventEntity -> FinancialEffectMapper.toDomain(entity, eventEntity)));
}

// Incorrecto: no existe @OneToMany en R2DBC reactivo
@OneToMany // prohibido
private List<Recovery> recoveries;
```

---

## 5) Repositorios R2DBC

### 5.1 Definicion del repositorio

```java
// En infrastructure/driven-adapters/r2dbc-repository
public interface FinancialEffectR2dbcRepository
        extends ReactiveCrudRepository<FinancialEffectEntity, Long> {

    // Busqueda por ID de negocio (no el PK tecnico)
    Mono<FinancialEffectEntity> findByFinancialEffectId(String financialEffectId);

    // Busqueda por FK
    Flux<FinancialEffectEntity> findByMaterializedEventId(String materializedEventId);

    // Query nativa para filtros compuestos
    @Query("""
            SELECT *
            FROM schgrcap.efecto_financiero
            WHERE id_compania_contable = :companyId
              AND fecha_contable BETWEEN :startDate AND :endDate
            ORDER BY fecha_creacion DESC
            """)
    Flux<FinancialEffectEntity> findByCompanyAndDateRange(
            @Param("companyId") Short companyId,
            @Param("startDate") LocalDateTime startDate,
            @Param("endDate") LocalDateTime endDate);
}
```

### 5.2 Reglas de los repositorios

- Extender `ReactiveCrudRepository<Entity, ID>` para operaciones CRUD basicas.
- Usar convenciones de nombres de Spring Data para queries derivadas: `findBy`, `findAllBy`, `existsBy`.
- Usar `@Query` con bloques de texto (`"""..."""`) para queries nativas complejas.
- Parametros con nombre usando `:nombreParametro` y `@Param`. No usar parametros posicionales `?1`.
- Dividir queries largas en multiples lineas. Maximo 120 caracteres por linea.
- Incluir siempre el esquema en las queries nativas: `FROM schgrcap.efecto_financiero`.

---

## 6) Convenciones de queries SQL

### 6.1 Formato general

- Palabras clave SQL en mayusculas: `SELECT`, `FROM`, `WHERE`, `JOIN`, `ORDER BY`.
- Nombres de tablas y columnas en minusculas siguiendo la convencion del esquema.
- Cada clausula principal en linea separada.
- Condiciones `AND` / `OR` al inicio de la linea siguiente, no al final.

```java
// Correcto
@Query("""
        SELECT ef.id_efecto_financiero,
               ef.valor_cop,
               ef.valor_usd,
               ef.fecha_contable
        FROM schgrcap.efecto_financiero ef
        WHERE ef.id_compania_contable = :companyId
          AND ef.fecha_contable >= :startDate
          AND ef.efecto_anulado IS NULL
        ORDER BY ef.fecha_creacion DESC
        """)

// Incorrecto: query en una sola linea
@Query("SELECT * FROM schgrcap.efecto_financiero WHERE id_compania_contable = :companyId AND fecha_contable >= :startDate AND efecto_anulado IS NULL")
```

### 6.2 Uso de indices existentes

Considerar los indices definidos en los DDLs del proyecto al escribir queries. Las columnas indexadas
deben aparecer en los filtros `WHERE` para aprovechar el indice. Consultar siempre los DDLs del
proyecto en curso para conocer los indices disponibles.

Ejemplo de indices del proyecto de referencia (esquema `schgrcap`):

| Tabla                  | Indice                                           | Columnas indexadas                        |
|------------------------|--------------------------------------------------|-------------------------------------------|
| `efecto_financiero`    | `idx_validacion_filtro`                          | `id_compania_contable`, `fecha_contable`  |
| `efecto_financiero`    | `idx_efecto_financiero_evento`                   | `id_evento_materializado`                 |
| `efecto_financiero`    | `idx_efecto_financiero_fecha_contable`           | `fecha_contable`                          |
| `recuperacion`         | `idx_recuperacion_efecto`                        | `id_efecto_financiero`                    |
| `evento_materializado` | `evento_materializado_idevento_materializado_idx`| `idevento_materializado`                  |
| `evento_materializado` | `evento_materializado_idmacroevento_idx`         | `idmacroevento`                           |

Reemplazar con los indices reales del proyecto antes de implementar queries de busqueda.

### 6.3 Paginacion reactiva

R2DBC no soporta `Pageable` de Spring Data directamente en queries nativas. Usar `LIMIT` y `OFFSET` explicitamente.

```java
@Query("""
        SELECT *
        FROM schgrcap.efecto_financiero
        WHERE id_compania_contable = :companyId
        ORDER BY fecha_creacion DESC
        LIMIT :limit OFFSET :offset
        """)
Flux<FinancialEffectEntity> findByCompanyPaginated(
        @Param("companyId") Short companyId,
        @Param("limit") int limit,
        @Param("offset") int offset);
```

---

## 7) Mapeo entre entidad y modelo de dominio

El mapeo es responsabilidad exclusiva del `Adapter`. Se implementa como una clase de utilidad estatica
en el mismo modulo `driven-adapters`.

```java
// En infrastructure/driven-adapters - clase de utilidad para mapeo
public class FinancialEffectMapper {

    private FinancialEffectMapper() {
        throw new IllegalStateException("Utility class");
    }

    public static FinancialEffect toDomain(FinancialEffectEntity entity) {
        return FinancialEffect.builder()
                .financialEffectId(entity.getFinancialEffectId())
                .materializedEventId(entity.getMaterializedEventId())
                .valueCop(entity.getValueCop())
                .valueUsd(entity.getValueUsd())
                .accountingDate(entity.getAccountingDate())
                .build();
    }

    public static FinancialEffectEntity toEntity(FinancialEffect domain) {
        var entity = new FinancialEffectEntity();
        entity.setFinancialEffectId(domain.getFinancialEffectId());
        entity.setMaterializedEventId(domain.getMaterializedEventId());
        entity.setValueCop(domain.getValueCop());
        entity.setValueUsd(domain.getValueUsd());
        entity.setAccountingDate(domain.getAccountingDate());
        entity.setCreationDate(OffsetDateTime.now());
        return entity;
    }
}
```

Reglas del mapper:
- Constructor privado con `throw new IllegalStateException("Utility class")`.
- Metodos estaticos unicamente.
- No contiene logica de negocio: solo transformacion de campos.
- El campo `fecha_creacion` se asigna en el mapper `toEntity`, no en el dominio.
- El campo `id` (PK tecnico) no se mapea al modelo de dominio. Es interno a la infraestructura.

---

## 8) Referencia de tablas del proyecto

Documentar aqui las tablas del proyecto en curso siguiendo el formato de la tabla de referencia.
Esta seccion debe actualizarse por el equipo al inicio de cada proyecto o cuando se agreguen nuevas tablas.

Formato obligatorio:

| Tabla | PK tecnico | ID de negocio | Descripcion |
|---|---|---|---|
| `nombre_tabla` | `columna` (tipo) | `columna_id_negocio` (tipo) si aplica | Descripcion del concepto de negocio |

Ejemplo basado en el proyecto de referencia (esquema `schgrcap`):

| Tabla                   | PK tecnico                        | ID de negocio                      | Descripcion                          |
|-------------------------|-----------------------------------|------------------------------------|--------------------------------------|
| `efecto_financiero`     | `id` (bigserial)                  | `id_efecto_financiero` (varchar)   | Efecto financiero de un evento       |
| `evento_materializado`  | `id_evento` (serial4)             | `idevento_materializado` (varchar) | Evento de riesgo materializado       |
| `macroevento`           | `id_macroevento_ppal` (bigserial) | `idmacroevento` (varchar)          | Macro evento de riesgo               |
| `recuperacion`          | `id` (bigserial)                  | `id_recuperacion` (varchar)        | Recuperacion de efecto financiero    |
| `m_tratamiento_contable`| `idtratamiento` (serial4)         | -                                  | Maestro de tratamiento contable      |
| `m_consecuencia`        | `id` (serial4)                    | -                                  | Maestro de consecuencias             |
| `m_linea_negocio`       | `idln` (serial4)                  | -                                  | Maestro de lineas de negocio         |
| `m_canal`               | `idcanal` (serial4)               | -                                  | Maestro de canales                   |
| `m_producto`            | `idprod` (serial4)                | -                                  | Maestro de productos                 |
| `m_geografia`           | `idgeografia` (serial4)           | -                                  | Maestro de geografia                 |

Poblar esta tabla con las entidades reales del proyecto antes de comenzar el desarrollo.

---

## 9) Cuando falte informacion de persistencia

Si una definicion de persistencia esta incompleta:
- Crear un `TODO` explicito indicando que columna, tabla o tipo falta definir.
- No asumir tipos de datos ni longitudes de columnas no documentadas en los DDLs.
- Formular 1-3 preguntas concretas al equipo de datos antes de implementar.
