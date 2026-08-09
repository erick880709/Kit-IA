# Diagramas adicionales en Mermaid: sintaxis y ejemplos

Complementan al C4 cuando este no cubre suficiente detalle sobre un flujo, el modelo de datos o la infraestructura. Inclúyelos solo cuando aporten información nueva — no dupliques en texto lo que el diagrama ya muestra.

## Diagramas de secuencia (obligatorios para flujos críticos)

Muestran el orden temporal de interacciones entre componentes/actores para UN caso de uso concreto. Son la herramienta más efectiva para explicar "qué pasa cuando el usuario hace X" — genera uno por cada flujo de negocio crítico (autenticación, el o los casos de uso principales, cualquier flujo con pasos asíncronos o múltiples servicios).

```mermaid
sequenceDiagram
    title Flujo: Creación de un Pedido

    actor Cliente
    participant WebApp as Aplicación Web
    participant API as API de Pedidos
    participant Validador as ValidadorPedido
    participant DB as Base de Datos
    participant Pasarela as Pasarela de Pago
    participant Cola as Cola de Mensajes
    participant Worker as Worker de Notificaciones

    Cliente->>WebApp: Confirma pedido
    WebApp->>API: POST /pedidos
    API->>Validador: validar(datosPedido)
    Validador-->>API: OK

    API->>Pasarela: Procesar pago
    Pasarela-->>API: Pago aprobado

    API->>DB: INSERT pedido
    DB-->>API: pedido creado (id)

    API->>Cola: Publica evento "PedidoCreado"
    API-->>WebApp: 201 Created (id pedido)
    WebApp-->>Cliente: Confirmación visual

    Cola->>Worker: Consume evento "PedidoCreado"
    Worker->>Worker: Genera email de confirmación
```

Buenas prácticas:
- Incluye rutas alternativas o de error cuando sean relevantes al negocio (ej. pago rechazado), usando `alt`/`else` de Mermaid, en vez de crear un diagrama separado para cada variante menor.
- En Caso B (AS-IS), el diagrama debe reflejar lo que el código hace realmente, incluyendo atajos o inconsistencias — no "limpies" el flujo al documentarlo.

## Diagrama de despliegue

> **Si el proveedor de nube es AWS, Azure o GCP, no uses Mermaid para este diagrama.** Genera un archivo `.drawio` con la iconografía oficial de cada proveedor — ver `references/drawio-iconos-nube.md` (y `references/guia-multi-cloud-deployment.md` / `references/guia-terraform-a-diagrama.md` según el caso). El `graph TB` de esta sección queda solo como **fallback** para infraestructura on-premise o proveedores sin librería de iconos disponible.

Útil cuando la topología de infraestructura no es obvia: múltiples ambientes, regiones, redes, orquestación de contenedores. Se puede modelar como un grafo con `graph` o con la sintaxis `C4Deployment` si el visor la soporta; `graph TB` es más portable:

```mermaid
graph TB
    subgraph "Región: us-east-1"
        subgraph "Cluster Kubernetes"
            subgraph "Namespace: produccion"
                pod1["Pod: API de Pedidos (x3 réplicas)"]
                pod2["Pod: Worker de Notificaciones (x2 réplicas)"]
            end
        end
        lb["Load Balancer"]
        rds[("RDS PostgreSQL - Multi-AZ")]
        redis[("ElastiCache Redis")]
    end

    cdn["CDN / CloudFront"]
    s3[("S3 - Assets estáticos")]

    Internet -->|HTTPS| cdn
    cdn --> s3
    Internet -->|HTTPS| lb
    lb --> pod1
    pod1 --> rds
    pod1 --> redis
    pod2 --> rds
```

## Diagrama entidad-relación

Solo si el modelo de datos es relevante y no trivial (más de 2-3 entidades con relaciones no obvias).

```mermaid
erDiagram
    CLIENTE ||--o{ PEDIDO : realiza
    PEDIDO ||--|{ ITEM_PEDIDO : contiene
    PRODUCTO ||--o{ ITEM_PEDIDO : referenciado_en
    PEDIDO }o--|| ESTADO_PEDIDO : tiene

    CLIENTE {
        uuid id PK
        string email
        string nombre
    }
    PEDIDO {
        uuid id PK
        uuid cliente_id FK
        decimal total
        string estado
        timestamp creado_en
    }
    ITEM_PEDIDO {
        uuid id PK
        uuid pedido_id FK
        uuid producto_id FK
        int cantidad
        decimal precio_unitario
    }
    PRODUCTO {
        uuid id PK
        string nombre
        decimal precio
        int stock
    }
```

## Diagrama de componentes/clases (fuera del C4 Nivel 4)

Si necesitas mostrar relaciones de herencia/composición más finas que el C4 Nivel 3, usa `classDiagram` (ver ejemplo completo en `diagramas-c4-ejemplos.md`, sección Nivel 4).

## Regla general

Cada diagrama de este archivo es condicional, a diferencia de los C4 (que siempre van niveles 1-3) y las secuencias de flujos críticos (que siempre van). Pregúntate: "¿este diagrama le dice al lector algo que el texto y los otros diagramas no le dicen ya?" Si la respuesta es no, no lo incluyas.
