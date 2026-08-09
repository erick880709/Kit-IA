# Cuestionario de Línea Base para Arquitectura de Software

Esto es lo primero que hay que relevar antes de proponer cualquier solución (Caso A) o antes de diseñar el TO-BE (Caso C). Está dividido en bloques temáticos para poder usarlo como checklist: primero se marca qué bloques ya responde la documentación encontrada en `resources/architecture/definitions/` o `resources/architecture/design/models/` (o el `.md` de especificaciones del usuario), y solo se pregunta lo que quede sin cubrir. No es un formulario que haya que disparar completo en cada corrida — es el inventario de preguntas posibles.

## 1. Contexto de negocio y alcance

- ¿Cuál es el objetivo del proyecto y qué problema de negocio resuelve?
- ¿Quiénes son los usuarios finales (internos, externos, B2B, B2C)?
- ¿Cuántos usuarios concurrentes/totales se esperan (actual y a 1-3 años)?
- ¿Existe un sistema legacy que se reemplaza o esto es greenfield puro?
- ¿Hay fecha límite (MVP, go-live) que condicione decisiones técnicas?
- ¿Cuál es el presupuesto disponible (licencias, infraestructura, personas)?

## 2. Lenguajes y stack tecnológico

- ¿Hay algún lenguaje/framework ya definido por política corporativa (Java, .NET, Node, Python, Go, etc.)?
- ¿El equipo tiene expertise previo en algún stack específico?
- ¿Se requiere reutilizar librerías, SDKs o componentes internos existentes?
- ¿Front-end: web, móvil nativo, híbrido, o los tres?
- ¿Se necesita soporte multiplataforma (iOS/Android/Web/Desktop)?

## 3. Arquitectura de la solución

- ¿Monolito, monolito modular, microservicios o serverless?
- ¿Se espera que el sistema escale horizontalmente?
- ¿Habrá comunicación síncrona (REST/gRPC) o asíncrona (eventos/colas)?
- ¿Se requiere arquitectura multi-tenant?
- ¿Hay integraciones con sistemas de terceros (ERP, CRM, pasarelas de pago)?
- ¿Se necesita API Gateway / BFF (Backend for Frontend)?

## 4. Nube e infraestructura

- ¿Cloud pública (AWS, Azure, GCP), on-premise, híbrida o multi-cloud?
- ¿Hay un proveedor ya contratado o preferido por la organización?
- ¿Se usarán contenedores (Docker) y orquestación (Kubernetes, ECS, etc.)?
- ¿Serverless (Lambda, Functions, Cloud Run) es una opción viable?
- ¿Requisitos de alta disponibilidad (SLA %, multi-región, multi-AZ)?
- ¿Estrategia de disaster recovery / RTO / RPO definidos?

## 5. DevOps y ciclo de entrega

- ¿Existe una cadena de CI/CD ya establecida? ¿Cuál herramienta (Jenkins, GitLab CI, GitHub Actions, Azure DevOps, ArgoCD)?
- ¿Infraestructura como código (Terraform, CloudFormation, Pulumi, Bicep)?
- ¿Gestión de configuración/secretos (Vault, AWS Secrets Manager, SOPS)?
- ¿Cuántos ambientes se manejan (dev, QA, staging, prod)?
- ¿Estrategia de branching (GitFlow, trunk-based)?
- ¿Frecuencia de despliegue esperada (continuo, semanal, por release)?

## 6. Base de datos y almacenamiento

- ¿Relacional (PostgreSQL, MySQL, SQL Server, Oracle) o NoSQL (MongoDB, DynamoDB, Cassandra)?
- ¿Volumen de datos esperado y proyección de crecimiento?
- ¿Se requiere caché (Redis, Memcached)?
- ¿Necesidad de búsqueda avanzada (Elasticsearch, OpenSearch)?
- ¿Se maneja Big Data / analítica (Data Warehouse, Data Lake)?
- ¿Requisitos de retención y backup de datos?

## 7. Seguridad y cumplimiento

- ¿Aplican regulaciones específicas (GDPR, PCI-DSS, HIPAA, ley local de datos personales)?
- ¿Estrategia de autenticación/autorización (OAuth2, SSO, MFA, IAM corporativo)?
- ¿Se requiere cifrado en tránsito y en reposo?
- ¿Hay políticas de seguridad ya definidas por un equipo de InfoSec?
- ¿Se necesitan pruebas de seguridad (SAST, DAST, pentesting) dentro del pipeline?

## 8. Calidad y pruebas

- ¿Qué nivel de cobertura de pruebas automatizadas se exige?
- ¿Se usarán pruebas unitarias, integración, end-to-end, carga/performance?
- ¿Herramientas de testing ya adoptadas (JUnit, Jest, Selenium, k6, JMeter)?
- ¿Existe un equipo de QA dedicado o es responsabilidad del equipo de desarrollo?

## 9. Observabilidad y operación

- ¿Herramientas de monitoreo/logging (Prometheus, Grafana, Datadog, ELK, CloudWatch)?
- ¿Se requiere tracing distribuido (Jaeger, OpenTelemetry)?
- ¿Hay un equipo de soporte/operaciones (SRE, NOC) y cómo se maneja on-call?
- ¿Definición de SLIs/SLOs esperados?

## 10. Equipo y gobernanza

- ¿Tamaño y composición del equipo (frontend, backend, DevOps, QA)?
- ¿Metodología de trabajo (Scrum, Kanban, SAFe)?
- ¿Existen estándares de arquitectura corporativos (guías, comités de arquitectura) que deban seguirse?
- ¿Quién es el dueño del producto y quién aprueba decisiones técnicas críticas?

## 11. Restricciones adicionales

- ¿Hay restricciones de licenciamiento (solo open source, prohibición de ciertos proveedores)?
- ¿Requisitos de accesibilidad (WCAG)?
- ¿Requisitos de internacionalización/localización (idiomas, monedas, zonas horarias)?
- ¿Existen dependencias con otros proyectos o equipos en paralelo?

## 12. Machine Learning / IA (solo si el sistema entrena o sirve un modelo propio)

> Ver `references/guia-ml-arquitectura.md` para el detalle de cada respuesta. Este bloque no aplica si el sistema únicamente consume una API de IA de terceros sin pipeline de datos ni fine-tuning propio.

- ¿Qué problema resuelve el modelo (clasificación, regresión, generación, recomendación) y cuál es la variable objetivo?
- ¿Qué fuentes de datos alimentan el entrenamiento (internas, públicas, de terceros) y quién es dueño de cada una?
- ¿Los datos incluyen información personal o sensible? ¿Qué marco normativo aplica (ley local de datos, GDPR, HIPAA) y existe ya la autorización/base legal necesaria?
- ¿Hay métricas objetivo definidas (F1, precisión, recall, AUC-ROC u otras) y sus valores meta?
- ¿El sistema requiere explicabilidad (XAI) ante el usuario final o ante un regulador?
- ¿El modelo es de apoyo a una decisión humana o autónomo?
- ¿Dónde y cómo se va a entrenar (cómputo disponible: CPU/GPU local, cloud, cluster)?
- ¿Existe ya una herramienta de tracking de experimentos o versionado de modelos/datos, o hay que definirla?
- ¿La inferencia en producción es en tiempo real, por lotes, o el alcance del proyecto es solo el modelo evaluado offline (sin despliegue)?
- ¿Hay estrategia prevista de reentrenamiento o monitoreo de deriva del modelo, o queda fuera de alcance por ahora?

## Cómo usar este cuestionario dentro del skill

1. Primero, coteja cada bloque contra lo que ya encontraste en `resources/architecture/definitions/`, `resources/design/models/` y el `.md` de especificaciones del usuario. Marca cada bloque como **cubierto**, **parcial** o **sin datos**.
2. Para los bloques **parciales** o **sin datos**, selecciona solo las preguntas relevantes al proyecto concreto (no todas aplican siempre — por ejemplo, "requisitos de accesibilidad" puede ser irrelevante para una API interna sin UI) y pregúntalas agrupadas por bloque, no una por una en mensajes separados.
3. Si el usuario no puede responder algo puntual y no es crítico (no cambia materialmente la arquitectura), regístralo como supuesto explícito en la sección 16 del documento en vez de bloquear la entrega.
4. Los bloques 1 a 4 (contexto de negocio, stack, arquitectura de la solución, nube) casi siempre son críticos — evita asumir sobre ellos sin preguntar. Los bloques 8 a 11 suelen admitir supuestos razonables documentados si el usuario no tiene la respuesta a mano. El bloque 12 (ML/IA) es crítico cuando aplica: las preguntas de datos sensibles/marco normativo y métricas objetivo no deben resolverse por supuesto — bloquean la arquitectura de entrenamiento si no están claras.
