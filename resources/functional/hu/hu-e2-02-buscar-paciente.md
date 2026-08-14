---
id: HU-E2-02
type: Historia de Usuario
epic: E2 - Flujo Clínico de Triaje
priority: Highest
points: 3
---

# HU-E2-02: Buscar paciente existente

## Como
Enfermera / Médico

## Quiero
buscar un paciente por documento, nombre o historia clínica

## Para
recuperar su información antes de crear un nuevo evento (RF-001).

## Criterios de Aceptación
- [ ] CA1: Búsqueda por documento exacto, nombre o apellidos parciales.
- [ ] CA2: Resultados paginados y con nombre completo visible en cabecera.
- [ ] CA3: Respuesta < 1 s (RNP-003).
- [ ] CA4: Si no hay resultados, ofrecer crear paciente (flujo HU-E2-01).

## Dependencias
HU-E2-01
