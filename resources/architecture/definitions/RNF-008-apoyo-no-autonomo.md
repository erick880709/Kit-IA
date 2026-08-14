# RNF-008: Sistema de Apoyo, No de Decisión Autónoma

**Tipo:** Requerimiento no funcional
**Categoría:** Seguridad / Cumplimiento normativo
**Fuente:** `context/CONTEXTO TRIAJE.txt` §9 · `context/01-CONTEXTO-MAESTRO-CONSOLIDADO.md` §2 · `context/CONTEXT TRIA.txt` (RNA-007)

## Descripción
El sistema es una herramienta de apoyo a la decisión clínica: el criterio del profesional prevalece siempre. El sistema nunca actúa de forma autónoma sobre la atención del paciente.

## Criterio medible / restricción concreta
- La clasificación del profesional es un campo propio, obligatorio, que el sistema nunca sobrescribe ni autocompleta.
- Modelos no validados clínicamente no se usan en producción (RNA-007).
- Toda sugerencia de IA se presenta como "sugerencia", con explicación y probabilidades visibles.

## Impacto en la arquitectura
El diseño del flujo de pantallas garantiza que la validación humana es paso obligatorio antes del cierre del evento (RF-011).

## Notas del analista
Este requisito es la base de gobernanza clínica del sistema y debe destacarse en el TFM como limitación/garantía ética.
