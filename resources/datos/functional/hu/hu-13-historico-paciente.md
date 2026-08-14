---
id: HU-13
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Media
points: 2
---

# HU-13: Histórico del paciente

## Como
Profesional sanitario

## Quiero
Buscar un paciente por número de documento y ver su historial completo de triajes previos: fechas, niveles asignados, concordancia IA-Profesional, y estado de cada episodio

## Para
Tener contexto clínico del paciente antes de iniciar un nuevo triaje, identificando patrones o recurrencias

## Criterios de Aceptación

- [ ] CA1: Campo de búsqueda por número de documento en la parte superior.
- [ ] CA2: Al buscar, se muestra un banner con los datos básicos del paciente: nombre completo, edad, EPS, grupo sanguíneo, alergias, total de episodios previos.
- [ ] CA3: **Tabla de triajes**: columnas con Fecha, Nivel IA, Nivel Profesional, Concordancia (✅/⚠️), Estado, Tiempo Total (min), y botón "📄 Ver Informe".
- [ ] CA4: Click en "📄 Ver Informe" descarga el informe HTML de ese triaje (`GET /api/reports/triage/{id}/download`).
- [ ] CA5: La tabla está ordenada por fecha descendente (más reciente primero).
- [ ] CA6: Si el documento no existe, se muestra mensaje "Paciente no encontrado".
- [ ] CA7: Si el paciente existe pero no tiene triajes, se muestra "Sin triajes registrados".

## Recurso de datos involucrado

- **Nombre del recurso:** Paciente, Triaje
- **Capa(s):** frontend (consume GET /api/patients/{id}/triages, GET /api/patients/{documento})

## Subtareas

- [ ] Crear `pages/HistoricoPacientePage.tsx`
- [ ] Implementar búsqueda por documento
- [ ] Implementar banner de datos del paciente
- [ ] Implementar tabla de triajes históricos
- [ ] Implementar descarga de informe individual
- [ ] Probar con paciente con y sin historial
