# Guía: Modo multi-nube (Caso A sin proveedor definido)

Se activa dentro del Caso A (proyecto nuevo) cuando, tras leer el `.md` de especificaciones, no hay un proveedor de nube determinado para el despliegue.

> Todos los nombres de archivo de esta guía (los tres `.drawio`, `Pricing_<Proyecto>.md`, `Arquitectura_Costos_<Proyecto>.html`) se guardan dentro de `resources/architecture/` — créala si no existe. Antes de generar los diagramas, valida/configura el MCP de diagramación siguiendo `references/guia-mcp-diagramacion.md` (usa `drawio-remoto` si está disponible).

## Cómo decidir si el proveedor está definido

Antes de asumir que falta, revisa si el `.md` de specs ya lo resuelve de alguna de estas formas (cualquiera de ellas cuenta como "definido", no actives el modo multi-nube):
- Menciona explícitamente AWS, Azure o GCP (o un servicio propio de una de ellas, ej. "usar Cognito para auth" implica AWS).
- Declara una restricción técnica que lo determina indirectamente (ej. "el equipo ya opera todo en Azure", "debe integrar con Google Workspace/BigQuery").
- El usuario lo indica en la conversación aunque no esté en el `.md`.

Si nada de esto aparece y el sistema efectivamente se va a desplegar en la nube (no on-premise, no edge/IoT puro), el proveedor **no está definido** → activa este modo.

Si es ambiguo (ej. el proyecto podría ir on-premise o en la nube y no se aclara), pregúntale al usuario en vez de asumir — es el mismo criterio que ya aplica el Paso 0 del skill para otras ambigüedades.

## Qué produce este modo

En vez de una única sección 12 (Vista de Despliegue) en el documento de arquitectura, produce:

1. **Tres diagramas de despliegue**, uno por proveedor, en formato `.drawio` con iconografía oficial (ver `references/drawio-iconos-nube.md`):
   - `Despliegue_AWS_<Proyecto>.drawio`
   - `Despliegue_Azure_<Proyecto>.drawio`
   - `Despliegue_GCP_<Proyecto>.drawio`
2. **Un archivo de pricing comparativo**: `Pricing_<Proyecto>.md` (ver `references/guia-pricing-cloud.md`).
3. **Un reporte HTML** que contextualiza cada arquitectura y compara costos: `Arquitectura_Costos_<Proyecto>.html` (ver `references/plantilla-reporte-costos.md`).
4. La sección 12 del documento principal (`Documento_Arquitectura_<Proyecto>.md`) no describe una sola infraestructura: resume que se evaluaron las tres nubes, enlaza a los tres `.drawio` y al reporte HTML, y remite la comparación de costo a `Pricing_<Proyecto>.md`.

## Paso 1 — Traducir la arquitectura lógica a cada proveedor

Parte de la Vista de Contenedores (C4 Nivel 2) ya definida — es la misma para las tres nubes, lo que cambia es qué **servicio administrado concreto** implementa cada contenedor. Usa esta tabla de equivalencias como punto de partida (ajústala si el proyecto tiene necesidades específicas que descarten una opción):

| Necesidad del contenedor | AWS | Azure | GCP |
|---|---|---|---|
| Cómputo con gestión de servidor | EC2 (+ Auto Scaling) | Virtual Machines (+ VMSS) | Compute Engine (+ MIG) |
| Cómputo en contenedores, sin servidor | ECS Fargate | Container Apps / AKS | Cloud Run / GKE |
| Funciones (event-driven) | Lambda | Functions | Cloud Functions |
| API Gateway | API Gateway | API Management | API Gateway |
| Balanceo de carga | Application Load Balancer | Application Gateway / Load Balancer | Cloud Load Balancing |
| Base de datos relacional administrada | RDS (Postgres/MySQL) | Azure SQL Database / Database for PostgreSQL | Cloud SQL |
| Base de datos NoSQL | DynamoDB | Cosmos DB | Firestore |
| Cache en memoria | ElastiCache (Redis) | Azure Cache for Redis | Memorystore |
| Almacenamiento de objetos | S3 | Blob Storage | Cloud Storage |
| Colas / mensajería | SQS / SNS | Service Bus | Pub/Sub |
| CDN | CloudFront | Azure CDN / Front Door | Cloud CDN |
| Identidad de usuarios finales | Cognito | Azure AD B2C / Entra External ID | Identity Platform |
| Observabilidad | CloudWatch | Azure Monitor | Cloud Monitoring |

Elige siempre el equivalente más directo (mismo nivel de gestión: si el contenedor pide "sin servidor", no propongas VMs en ninguna nube). No optimices de más: el objetivo es una comparación justa, no la mejor arquitectura posible en cada nube por separado.

## Paso 2 — Generar los tres diagramas

Para cada proveedor, sigue `references/drawio-iconos-nube.md` con los nombres reales del proyecto (no los genéricos de este documento). Mantén la topología equivalente entre los tres (mismos límites lógicos: red privada, subred pública/privada, zona de alta disponibilidad) para que la comparación sea legible.

## Paso 3 — Pricing

Sigue `references/guia-pricing-cloud.md` íntegro. Los servicios a cotizar en cada proveedor salen directamente de los nodos de cada diagrama del Paso 2.

## Paso 4 — Reporte HTML

Sigue `references/plantilla-reporte-costos.md`. Reutiliza el mismo XML de cada `.drawio` y las mismas cifras de `Pricing_<Proyecto>.md` — no generes números nuevos en el HTML.

## Paso 5 — Enlazar todo desde el documento principal

En la sección 12 (Vista de Despliegue) de `Documento_Arquitectura_<Proyecto>.md`, agrega una nota como:

> No se definió un proveedor de nube en las especificaciones. Se evaluaron AWS, Azure y GCP con arquitecturas equivalentes — ver diagramas `Despliegue_AWS_<Proyecto>.drawio`, `Despliegue_Azure_<Proyecto>.drawio`, `Despliegue_GCP_<Proyecto>.drawio`, el comparativo de costos en `Pricing_<Proyecto>.md`, y el reporte consolidado en `Arquitectura_Costos_<Proyecto>.html`.

Y añade una recomendación explícita (no dejes la decisión abierta sin opinión): cuál de las tres conviene dado el contexto del proyecto (costo, requerimientos no funcionales, restricciones del equipo), y qué tendría que cambiar para que la recomendación cambiara.
