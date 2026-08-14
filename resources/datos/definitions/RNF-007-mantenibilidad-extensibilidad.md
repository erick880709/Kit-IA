# RNF-007: Mantenibilidad y Extensibilidad

**Tipo:** Requerimiento no funcional
**Categoría:** Mantenibilidad
**Fuente:** CONTEXT TRIA.txt — Sección 18, OC-008; 01-CONTEXTO-MAESTRO-CONSOLIDADO.md

## Descripción
El sistema debe diseñarse con una arquitectura modular que permita la evolución independiente de sus componentes (captura de datos, motor IA, explicabilidad, auditoría, interfaz de usuario), facilitando el reemplazo de modelos, la adición de nuevas variables predictoras, la integración futura con HCE y la adaptación a diferentes IPS sin cambios de código.

## Criterio medible / restricción concreta
- **OC-008 — Mantenibilidad y extensibilidad:**
  - El motor de IA debe ser intercambiable (cambio de modelo activo sin modificar la aplicación principal — RF-MOD-003/004 ya lo habilitan).
  - Las variables de entrada al modelo deben ser configurables (añadir/quitar features sin cambios de código en la UI).
  - Los catálogos clínicos (motivos de consulta, antecedentes, niveles de conciencia) deben ser administrables sin despliegues (RF-SEC-002 menciona administración de catálogos; el módulo de Configuración Clínica sugerido en la Entrega 7 lo formaliza).
  - El sistema debe ser independiente de una IPS específica: rangos de signos vitales, umbrales de alerta y catálogos son parametrizables por institución.
- El código fuente debe estar organizado en módulos con responsabilidades claras y acoplamiento bajo (separación de concerns: UI / lógica de negocio / acceso a datos / motor IA).
- La documentación de arquitectura debe incluir diagramas de componentes y dependencias.

## Impacto en la arquitectura
- Patrón de arquitectura por capas o hexagonal (ports & adapters) para desacoplar el motor IA del resto del sistema.
- API REST entre el frontend y el backend, y entre el backend y el motor IA, permitiendo que cada componente evolucione independientemente.
- Configuración externalizada (archivos YAML/JSON, variables de entorno) para parámetros clínicos y de modelo.

## Notas del analista
- La mantenibilidad es particularmente importante para un TFM: el código será evaluado por un tribunal y potencialmente retomado por otros investigadores. Un código limpio, modular y bien documentado es parte de la calidad académica del trabajo.
- La recomendación de añadir un módulo de Configuración Clínica (Entrega 7 del documento maestro) es acertada para producción, pero puede quedar como trabajo futuro para la demo.
