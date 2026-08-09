# Diagramas C4 en Mermaid: sintaxis y ejemplos

El C4 Model describe un sistema en 4 niveles de zoom creciente: Contexto → Contenedores → Componentes → Código. Genera siempre los tres primeros; el cuarto es opcional. Usa la sintaxis `C4Context`, `C4Container`, `C4Component` de Mermaid (soportada de forma nativa, se renderiza en GitHub, GitLab y la mayoría de visores de Markdown modernos).

## Nivel 1 — Diagrama de Contexto

Muestra el sistema como una caja negra y sus actores/sistemas externos. Responde: "¿con quién interactúa el sistema y para qué?"

```mermaid
C4Context
    title Diagrama de Contexto del Sistema - [Nombre del Sistema]

    Person(cliente, "Cliente", "Usuario final que realiza compras")
    Person(admin, "Administrador", "Gestiona catálogo y pedidos")

    System(sistema, "[Nombre del Sistema]", "Permite gestionar el ciclo completo de pedidos online")

    System_Ext(pasarelaPago, "Pasarela de Pago", "Procesa transacciones (ej. Stripe)")
    System_Ext(sistemaEnvios, "Proveedor de Envíos", "Genera guías y rastrea entregas")
    System_Ext(email, "Servicio de Email", "Envía notificaciones transaccionales")

    Rel(cliente, sistema, "Realiza pedidos, consulta estado")
    Rel(admin, sistema, "Administra catálogo y pedidos")
    Rel(sistema, pasarelaPago, "Procesa pagos", "HTTPS/API")
    Rel(sistema, sistemaEnvios, "Solicita guías de envío", "HTTPS/API")
    Rel(sistema, email, "Envía notificaciones", "SMTP/API")
```

## Nivel 2 — Diagrama de Contenedores

Abre la caja negra del sistema en las aplicaciones/servicios/bases de datos que lo componen (los "contenedores" desplegables de forma independiente).

```mermaid
C4Container
    title Diagrama de Contenedores - [Nombre del Sistema]

    Person(cliente, "Cliente")

    System_Boundary(sistema, "[Nombre del Sistema]") {
        Container(webApp, "Aplicación Web", "React/Next.js", "Interfaz de usuario para clientes")
        Container(api, "API de Pedidos", "Node.js/Express", "Expone la lógica de negocio vía REST")
        Container(workerNotif, "Worker de Notificaciones", "Node.js", "Procesa cola de eventos y envía notificaciones")
        ContainerDb(db, "Base de Datos", "PostgreSQL", "Almacena pedidos, clientes y catálogo")
        ContainerDb(cache, "Cache", "Redis", "Cachea catálogo y sesiones")
        Container(cola, "Cola de Mensajes", "RabbitMQ", "Desacopla eventos de pedido")
    }

    System_Ext(pasarelaPago, "Pasarela de Pago")

    Rel(cliente, webApp, "Usa", "HTTPS")
    Rel(webApp, api, "Consume", "JSON/HTTPS")
    Rel(api, db, "Lee/escribe", "SQL")
    Rel(api, cache, "Lee/escribe", "Redis Protocol")
    Rel(api, cola, "Publica eventos de pedido")
    Rel(cola, workerNotif, "Consume eventos")
    Rel(api, pasarelaPago, "Procesa pagos", "HTTPS/API")
```

## Nivel 3 — Diagrama de Componentes

Abre UN contenedor específico (normalmente el más complejo o crítico) en sus módulos/componentes internos y cómo colaboran. Genera uno por cada contenedor no trivial — no fuerces este nivel para contenedores simples como una base de datos administrada.

```mermaid
C4Component
    title Diagrama de Componentes - API de Pedidos

    Container(webApp, "Aplicación Web")
    ContainerDb(db, "Base de Datos")
    Container(cola, "Cola de Mensajes")

    Container_Boundary(api, "API de Pedidos") {
        Component(controller, "PedidosController", "Express Router", "Recibe y valida peticiones HTTP")
        Component(servicio, "PedidosService", "Clase de dominio", "Orquesta la lógica de negocio de pedidos")
        Component(repo, "PedidosRepository", "Patrón Repository", "Abstrae el acceso a datos de pedidos")
        Component(validador, "ValidadorPedido", "Módulo de dominio", "Aplica reglas de negocio de validación")
        Component(publicador, "EventPublisher", "Adaptador", "Publica eventos de dominio en la cola")
    }

    Rel(webApp, controller, "Envía petición", "JSON/HTTPS")
    Rel(controller, servicio, "Invoca")
    Rel(servicio, validador, "Valida reglas de negocio")
    Rel(servicio, repo, "Persiste/consulta")
    Rel(repo, db, "SQL")
    Rel(servicio, publicador, "Notifica evento de dominio")
    Rel(publicador, cola, "Publica mensaje")
```

## Nivel 4 — Diagrama de Código (opcional)

Solo si el usuario lo pide o un componente es crítico/complejo. Usa un diagrama de clases estándar de Mermaid (`classDiagram`), no la sintaxis C4:

```mermaid
classDiagram
    class PedidosService {
        -PedidosRepository repo
        -ValidadorPedido validador
        +crearPedido(datos) Pedido
        +cancelarPedido(id) void
    }
    class PedidosRepository {
        <<interface>>
        +guardar(pedido) void
        +buscarPorId(id) Pedido
    }
    class ValidadorPedido {
        +validar(pedido) ResultadoValidacion
    }
    PedidosService --> PedidosRepository
    PedidosService --> ValidadorPedido
```

## Reglas prácticas

- Usa nombres reales del dominio/proyecto en los diagramas, nunca los genéricos de estos ejemplos.
- En Caso B (AS-IS), cada relación (`Rel`) del diagrama debe poder señalarse a una línea de código o configuración real — si no puedes verificarla, no la incluyas o márcala como supuesto.
- Mantén cada diagrama enfocado: un Nivel 2 con más de ~10 contenedores probablemente necesita agruparse (ej. por dominio/bounded context) en vez de mostrar todo de una vez.
