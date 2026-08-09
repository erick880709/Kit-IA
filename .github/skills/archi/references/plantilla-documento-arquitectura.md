# Plantilla: Documento de Arquitectura de Software

Esqueleto de referencia inspirado en arc42 y en el C4 Model de Simon Brown. Adapta las secciones al caso (A: nuevo, B: AS-IS, C: TO-BE) — omite lo que no aplique en vez de rellenarlo con texto genérico. El texto entre `[...]` es guía para ti, no debe aparecer en el documento final.

```markdown
# Documento de Arquitectura de Software: [Nombre del Proyecto]

**Versión:** [1.0]
**Fecha:** [fecha]
**Tipo de documento:** [Arquitectura propuesta / AS-IS / TO-BE]
**Autor:** [nombre o "Generado con asistencia de IA, revisado por —"]

## 1. Introducción y Objetivos

### 1.1 Propósito del sistema
[Qué problema de negocio resuelve, en 2-4 líneas.]

### 1.2 Requerimientos funcionales clave
[Lista priorizada, no exhaustiva — los 5-10 que definen la forma del sistema.]

### 1.3 Atributos de calidad (requerimientos no funcionales)
[Tabla: atributo | prioridad | métrica/objetivo concreto. Ej: Disponibilidad | Alta | 99.9% mensual.]

### 1.4 Interesados (stakeholders)
[Quién usa, opera y decide sobre el sistema.]

## 2. Restricciones

[Restricciones técnicas, organizacionales, de presupuesto, de plazo o normativas que limitan las opciones de diseño. Sé específico: "el equipo tiene experiencia solo en Node.js" es una restricción real, "debe ser escalable" no lo es (eso es un atributo de calidad, va en 1.3).]

## 3. Alcance y Contexto del Sistema

### 3.1 Contexto de negocio
[Actores externos, sistemas con los que integra, límites de responsabilidad del sistema.]

### 3.2 Diagrama de Contexto (C4 Nivel 1)
[Diagrama Mermaid — ver references/diagramas-c4-ejemplos.md]

## 4. Estrategia de Solución

[La decisión arquitectónica de más alto nivel y su justificación: estilo arquitectónico elegido (monolito modular, microservicios, event-driven, serverless, etc.), y por qué — ligado directamente a los atributos de calidad de la sección 1.3, no a preferencia personal ni moda.]

## 5. Vista de Contenedores (C4 Nivel 2)

[Diagrama Mermaid de contenedores — aplicaciones, servicios, bases de datos, cómo se comunican.]

Para cada contenedor: responsabilidad, tecnología, y por qué esa tecnología.

## 6. Vista de Componentes (C4 Nivel 3)

[Un diagrama de componentes por cada contenedor no trivial. No generes este nivel para contenedores triviales (ej. una base de datos administrada) — solo para los que tienen lógica interna relevante.]

## 7. [Opcional] Vista de Código (C4 Nivel 4)

[Solo si aplica: diagrama de clases para el componente más crítico o complejo.]

## 8. Vistas de Ejecución: Diagramas de Secuencia

[Un diagrama de secuencia por cada flujo/caso de uso crítico identificado. Antes de cada diagrama, una línea de contexto: qué caso de uso representa y por qué es crítico.]

## 9. Modelo de Datos

[Solo si es relevante y no trivial. Diagrama entidad-relación + descripción de las entidades principales y sus relaciones. Incluye decisiones de particionamiento/sharding o estrategias de caché si aplican.]

## 10. Conceptos Transversales

[Cómo se resuelven, de forma consistente en todo el sistema: autenticación/autorización, manejo de errores y resiliencia, logging/observabilidad, gestión de configuración y secretos, validación.]

## 11. Decisiones Arquitectónicas (ADRs)

[Una entrada por decisión importante. Formato compacto:]

### ADR-001: [Título de la decisión]
- **Contexto:** [qué problema forzó la decisión]
- **Decisión:** [qué se decidió]
- **Alternativas consideradas:** [y por qué se descartaron]
- **Consecuencias:** [positivas y negativas — toda decisión real tiene ambas]

## 12. Vista de Despliegue

[Diagrama de despliegue solo si la infraestructura no es obvia o tiene detalles relevantes: ambientes, regiones, estrategia de contenedores/orquestación, redes.]

[Si el proveedor de nube es AWS, Azure o GCP, el diagrama va en formato `.drawio` con iconografía oficial (ver references/drawio-iconos-nube.md) en vez de Mermaid — enlaza aquí el archivo `.drawio` correspondiente. Si en Caso A no había proveedor definido en las especificaciones, esta sección resume el modo multi-nube en vez de una sola infraestructura: ver references/guia-multi-cloud-deployment.md para la estructura exacta (tres diagramas, Pricing_<Proyecto>.md, y el reporte Arquitectura_Costos_<Proyecto>.html). En Caso B/C, si el diagrama se generó a partir de código Terraform por ausencia de documentación previa, dilo explícitamente y referencia la ruta del código (ver references/guia-terraform-a-diagrama.md). Usa Mermaid `graph TB` (ver references/diagramas-adicionales-ejemplos.md) solo cuando la infraestructura no corresponda a AWS/Azure/GCP (on-premise, proveedor sin librería de iconos disponible).]

## 13. Riesgos y Deuda Técnica

[Riesgos técnicos identificados con su impacto y mitigación propuesta. En AS-IS, esta sección es principalmente deuda técnica encontrada; en propuestas nuevas, son riesgos de la solución elegida.]

## 14. [Solo Caso C — TO-BE] Análisis de Brechas (Gap Analysis)

[Ver references/guia-as-is-to-be.md para la estructura detallada.]

## 15. [Solo Caso C — TO-BE] Roadmap de Migración

[Ver references/guia-as-is-to-be.md.]

## 16. Supuestos

[Todo lo que asumiste por falta de información explícita en las especificaciones o en el código. Sé honesto aquí — es lo que más valor le da al lector para saber qué validar.]

## 17. Glosario

[Solo términos de dominio o siglas que no sean evidentes.]
```
