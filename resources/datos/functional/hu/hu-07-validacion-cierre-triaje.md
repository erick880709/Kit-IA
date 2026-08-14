---
id: HU-07
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Alta
points: 5
---

# HU-07: Validación y cierre de triaje

## Como
Profesional sanitario (médico/a o enfermero/a senior)

## Quiero
Revisar el nivel sugerido por la IA, compararlo con mi clasificación profesional, confirmar o reclasificar el triaje, y cerrar el episodio

## Para
Garantizar que la decisión final del nivel de triaje es validada por un profesional humano, manteniendo la seguridad del paciente y la trazabilidad de la decisión

## Criterios de Aceptación

- [ ] CA1: La página muestra un resumen completo del triaje: datos del paciente, signos vitales, evaluación clínica, nivel IA sugerido (con probabilidades), y nivel profesional (si ya fue asignado).
- [ ] CA2: **Visualización del flujo**: componente `TriageStateMachine` que muestra el progreso en los 5 pasos del triaje con checkmarks en los completados.
- [ ] CA3: **Indicador de concordancia**: si el nivel IA y el nivel profesional coinciden → ✅ "Concordancia IA-Profesional". Si difieren → ⚠️ "Discrepancia" con ambos niveles resaltados.
- [ ] CA4: **Reclasificación**: el profesional puede cambiar el nivel asignado mediante un select. Esto registra una reclasificación en el historial (usa `POST /api/triages/{id}/reclassify`).
- [ ] CA5: **Cierre del triaje**:
  - Select de motivo de cierre (opcional).
  - Botón "✅ Cerrar Triaje" que llama a `POST /api/triages/{id}/close`.
  - Al cerrar, se muestra animación de confirmación (🎉) y se habilita la descarga del informe.
- [ ] CA6: **Descarga de informe** (`GET /api/reports/triage/{id}/download`):
  - Botón "📄 Descargar Informe" que descarga un archivo HTML con el resumen completo del triaje.
- [ ] CA7: **Checklist de prerequisitos**: antes de permitir el cierre, se verifica que todos los pasos anteriores estén completos. Si falta alguno, se muestra un warning con el paso faltante.
- [ ] CA8: Al cerrar, el triaje activo se limpia del contexto y se redirige al dashboard o a registrar nuevo paciente.

## Recurso de datos involucrado

- **Nombre del recurso:** Triaje (cierre)
- **Capa(s):** frontend (consume POST /api/triages/{id}/close, GET /api/reports/triage/{id}/download)

## Subtareas

- [ ] Crear `pages/TriageValidationPage.tsx`
- [ ] Crear `components/clinical/TriageStateMachine.tsx` (visualización de pasos)
- [ ] Implementar indicador de concordancia
- [ ] Implementar flujo de reclasificación
- [ ] Implementar cierre con animación
- [ ] Implementar descarga de informe HTML
- [ ] Implementar checklist de prerequisitos
- [ ] Probar flujo completo de cierre
