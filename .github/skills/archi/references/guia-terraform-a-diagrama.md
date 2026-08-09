# Guía: Generar el diagrama de despliegue desde código Terraform

Aplica en Caso B (y en la parte AS-IS del Caso C) cuando **no existe un documento de arquitectura de despliegue** vigente para el proyecto. Antes de usar esta guía, confirma que de verdad no existe: busca en `/docs`, README, `resources/architecture/` y cualquier `Documento_Arquitectura_*.md` / `Arquitectura_AS-IS_*.md` previo que ya declare proveedor de nube y componentes. Si existe y es consistente con el código actual, úsalo como fuente de verdad y no regeneres nada de esta guía.

> El `.drawio` que produzca esta guía se guarda dentro de `resources/architecture/` (créala si no existe). Antes de generarlo, valida/configura el MCP de diagramación siguiendo `references/guia-mcp-diagramacion.md` (usa `drawio-remoto` si está disponible).

## Regla de oro

El diagrama se construye **solo con lo que el `.tf` declara explícitamente**. Si un recurso no está en el código (por ejemplo, se creó manualmente en la consola y no está importado a Terraform), no aparece en el diagrama — o aparece marcado como "fuera de Terraform / gestionado manualmente" si hay evidencia indirecta de su existencia (ej. un `data source` que lo referencia). Nunca completes huecos por intuición del nombre de una carpeta o módulo.

## Paso 1 — Localizar el código Terraform

Busca archivos `.tf` y `.tf.json` en el repositorio (rutas típicas: `terraform/`, `infra/`, `infrastructure/`, `iac/`, o la raíz del repo). Si el repo es grande, usa un agente de exploración (`Explore`/`general-purpose`) para listar todos los `.tf` y sus rutas antes de leerlos uno por uno.

Si hay múltiples entornos (`environments/dev`, `environments/prod`, workspaces) o múltiples stacks/módulos raíz, documenta el diagrama del entorno de **producción** por defecto, salvo que el usuario pida otro explícitamente. Si no es identificable cuál es producción, pregúntale.

## Paso 2 — Identificar el proveedor de nube

Busca el bloque `provider` (o `required_providers` en Terraform ≥ 0.13):

```hcl
terraform {
  required_providers {
    aws = { source = "hashicorp/aws" }
  }
}
provider "aws" {
  region = "us-east-1"
}
```

- `provider "aws"` → AWS, usa `mxgraph.aws4.*` (ver `references/drawio-iconos-nube.md`).
- `provider "azurerm"` → Azure, usa `mxgraph.azure.*`.
- `provider "google"` / `provider "google-beta"` → GCP, usa `mxgraph.gcp2.*`.

Si hay más de un provider (multi-cloud real, no el modo comparativo del Caso A), genera un `.drawio` por proveedor presente, reflejando solo lo que ese provider gestiona.

## Paso 3 — Mapear recursos a componentes del diagrama

Recorre los bloques `resource "<tipo>" "<nombre>" { ... }` y agrúpalos por función, no por tipo técnico exacto. Tabla de mapeo para los tipos más comunes (AWS; el mismo criterio aplica a `azurerm_*` y `google_*` con sus equivalentes):

| Tipo de recurso Terraform | Rol en el diagrama | Shape sugerido |
|---|---|---|
| `aws_instance`, `aws_launch_template`, `aws_autoscaling_group` | Cómputo | `mxgraph.aws4.ec2` |
| `aws_ecs_service`, `aws_ecs_task_definition` | Cómputo en contenedores | `mxgraph.aws4.elastic_container_service` |
| `aws_lambda_function` | Función | `mxgraph.aws4.lambda` |
| `aws_lb`, `aws_alb` | Balanceador | `mxgraph.aws4.application_load_balancer` |
| `aws_apigatewayv2_api`, `aws_api_gateway_rest_api` | API Gateway | `mxgraph.aws4.api_gateway` |
| `aws_db_instance`, `aws_rds_cluster` | Base de datos | `mxgraph.aws4.relational_database_service` |
| `aws_dynamodb_table` | Base de datos NoSQL | `mxgraph.aws4.dynamodb` |
| `aws_elasticache_cluster`, `aws_elasticache_replication_group` | Cache | `mxgraph.aws4.elasticache` |
| `aws_s3_bucket` | Almacenamiento | `mxgraph.aws4.simple_storage_service` |
| `aws_sqs_queue` | Cola | `mxgraph.aws4.simple_queue_service` |
| `aws_sns_topic` | Notificación/eventos | `mxgraph.aws4.simple_notification_service` |
| `aws_cloudfront_distribution` | CDN | `mxgraph.aws4.cloudfront` |
| `aws_vpc` | Contenedor de red | `mxgraph.aws4.group` (`grIcon=group_vpc`) |
| `aws_subnet` | Subred (pública si tiene ruta a IGW, privada si no) | agrupación dentro de la VPC |
| `aws_cognito_user_pool` | Identidad | `mxgraph.aws4.cognito` |

Para `azurerm_*`: `azurerm_linux_virtual_machine`/`azurerm_windows_virtual_machine` → VM, `azurerm_app_service` → App Service, `azurerm_kubernetes_cluster` → AKS, `azurerm_postgresql_flexible_server`/`azurerm_mssql_database` → base de datos, `azurerm_redis_cache` → cache, `azurerm_storage_account` → storage, `azurerm_servicebus_namespace` → mensajería, `azurerm_virtual_network` → contenedor de red.

Para `google_*`: `google_compute_instance` → Compute Engine, `google_cloud_run_service` → Cloud Run, `google_container_cluster` → GKE, `google_cloudfunctions_function` → Cloud Functions, `google_sql_database_instance` → Cloud SQL, `google_firestore_database` → Firestore, `google_storage_bucket` → Cloud Storage, `google_pubsub_topic` → Pub/Sub, `google_compute_network` → VPC.

Si aparece un `resource` que no tiene equivalente evidente en la tabla, no lo omitas: inclúyelo con el shape genérico del proveedor y su tipo real como etiqueta, en vez de forzarlo a una categoría incorrecta.

## Paso 4 — Reconstruir las relaciones

Las conexiones del diagrama salen de las referencias entre recursos dentro del propio `.tf` (no de suposiciones):
- Un recurso que referencia el `id`/`arn` de otro (ej. `subnet_id = aws_subnet.privada.id`, `vpc_security_group_ids = [aws_security_group.api.id]`) implica una relación de red/pertenencia.
- Variables de entorno o configuración que apuntan a un endpoint (ej. `environment { variables = { DB_HOST = aws_db_instance.principal.address } }`) implican una relación de comunicación aplicativa — inclúyela como flecha con la etiqueta del propósito (ej. "Lee/escribe", "SQL").
- Si dos recursos están en el mismo `.tf` pero no hay ninguna referencia cruzada entre ellos, no dibujes una conexión — no está soportada por el código.

## Paso 5 — Generar el archivo y documentar hallazgos

1. Genera `Despliegue_<Proveedor>_<Proyecto>.drawio` siguiendo `references/drawio-iconos-nube.md`.
2. En la sección 12 del documento AS-IS, referencia el archivo y anota explícitamente: "Diagrama generado a partir del código Terraform en `<ruta>`, módulo/entorno `<nombre>`". Esto deja claro que es una fuente verificable, no una inferencia.
3. Si durante el análisis encuentras recursos con configuración hardcodeada, ausencia de tags, secretos en texto plano, o módulos sin versión fijada, regístralo en la sección 13 (Riesgos y Deuda Técnica) del documento — es información valiosa que ya estás viendo de todas formas.

## Si no hay Terraform ni documento previo

Antes de dejar la sección de despliegue vacía, busca otras señales de IaC (CloudFormation `.yaml`/`.json` con `AWSTemplateFormatVersion`, ARM/Bicep, Pulumi, manifiestos de Kubernetes con anotaciones de nube, `serverless.yml`). Si encuentras alguna, aplica el mismo criterio de esta guía adaptado a esa herramienta. Si no hay ninguna evidencia de infraestructura como código, pregúntale al usuario en qué nube/infraestructura se despliega hoy, o documenta explícitamente en la sección 16 (Supuestos) que la infraestructura de despliegue no pudo determinarse a partir del repositorio.
