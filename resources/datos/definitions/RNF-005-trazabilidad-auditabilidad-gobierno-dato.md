# RNF-005: Trazabilidad, Auditabilidad y Gobierno del Dato

**Tipo:** Requerimiento no funcional
**Categoría:** Auditoría / Gobierno del Dato
**Fuente:** CONTEXT TRIA.txt — Secciones 18 (OC-004), 34 (RNAU-001 a 006), 35 (RNGD-001 a 006), 36 (RNQ-001 a 006)

## Descripción
El sistema debe garantizar trazabilidad completa de cada acción, decisión y modificación, permitiendo auditorías clínicas y técnicas en cualquier momento. El gobierno del dato asegura que cada variable tenga un propietario funcional definido, una definición oficial y trazabilidad desde su origen hasta su uso en inferencias.

## Criterio medible / restricción concreta
- **OC-004 — Trazabilidad completa:** Toda acción sobre un evento de triaje debe ser trazable hasta el usuario, timestamp, acción realizada, valor anterior y nuevo (si aplica), y modelo/versión utilizado (si aplica).
- **RNAU-001 a 006:** Cada inferencia, modificación clínica, cambio de modelo activo y acceso a datos sensibles genera un registro de auditoría inmutable. Los registros son consultables por filtros y exportables. No se permite eliminación de registros.
- **RNGD-001 a 006:** Toda variable del modelo de datos tiene propietario funcional y definición oficial. No existen atributos duplicados con diferente significado. Los catálogos se administran centralmente. Las modificaciones estructurales requieren control de cambios.
- **RNQ-001 a 006:** Los campos obligatorios no se almacenan vacíos. Los datos se validan antes de la inferencia. Valores fuera de rango generan alertas. Variables categóricas usan catálogos controlados. Fechas/horas en formato no ambiguo. Detección de registros duplicados.

## Impacto en la arquitectura
- Los registros de auditoría deben almacenarse en un almacén separado (tabla/colección de solo inserción) con políticas de retención.
- La integridad referencial entre evento de triaje, predicción, modelo y auditoría es crítica.
- El catálogo de datos debe estar documentado como código (data dictionary en formato estructurado, versionado junto con el código fuente).
- La validación de calidad del dato debe ejecutarse en dos capas: frontend (experiencia de usuario inmediata) y backend (validación de integridad antes de la inferencia).

## Notas del analista
- La trazabilidad es el mecanismo que habilita la detección de deriva (RNA-010) y la comparativa IA vs. profesional (RF-REP-005). Sin trazabilidad, no hay forma de medir el desempeño real del sistema.
- El catálogo de datos (`03-CATALOGO-DATOS-Y-VARIABLES.md`) ya resuelve la trazabilidad de fuentes de datos reales. Falta la trazabilidad a nivel de código (qué endpoint usa qué campo de qué fuente) — eso corresponde a la documentación técnica, no a este RNF.
