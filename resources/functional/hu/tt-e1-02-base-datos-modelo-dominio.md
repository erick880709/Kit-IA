---
id: TT-E1-02
type: Tarea Técnica
epic: E1 - Fundación del Sistema
priority: Highest
points: 8
---

# TT-E1-02: Configurar base de datos y modelo de dominio (ENT-001 a ENT-012)

## Descripción
Implementar el esquema SQLite del modelo de dominio completo (catálogo ENT-001..012 de RD-002), con migración no destructiva y catálogos controlados.

## Criterios de Done
- [ ] Tablas para ENT-001 Paciente (con ViaLlegada, EpisodiosPreviosUrgencias y los 9 campos de TT-E7-01), ENT-002 EventoTriaje (registro dual de RD-003), ENT-003 SignosVitales, ENT-004 MotivoConsulta, ENT-005 Antecedentes, ENT-008 TextoClinico, ENT-009 Modelo, más entidades 006-012 según CONTEXT TRIA.txt.
- [ ] Catálogos controlados: VIA_LLEGADA, NIVELES_TRIAGE (I-V), DEPARTAMENTOS_COLOMBIA (32), CIUDADES_POR_DEPARTAMENTO (~200).
- [ ] Migración idempotente (`ADD COLUMN IF NOT EXISTS`).
- [ ] ControlCambios habilitado para entidades clínicas.

## Recurso de datos involucrado
### Recurso
- **Nombre:** Entidades del dominio ENT-001..ENT-012
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| (ver RD-002 y RD-003) | — | — | Esquema completo en `resources/design/models/RD-002` y `RD-003` |

### Relaciones con otros recursos
- `Paciente` (1:N) `EventoTriaje`
- `EventoTriaje` (1:N) `SignosVitales`, `MotivoConsulta`, `Antecedentes`, `TextoClinico`

## Dependencias
TT-E1-01

## Subtareas
- [ ] Script de creación de esquema y catálogos
- [ ] Migración para los 9 campos de Paciente (TT-E7-01)
- [ ] Seeds de catálogos y datos sintéticos
- [ ] Test de integridad referencial
