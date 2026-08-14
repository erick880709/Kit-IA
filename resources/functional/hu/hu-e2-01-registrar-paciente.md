---
id: HU-E2-01
type: Historia de Usuario
epic: E2 - Flujo Clínico de Triaje
priority: Highest
points: 5
---

# HU-E2-01: Registrar paciente con búsqueda de duplicados y vía de llegada

## Como
Enfermera / personal administrativo

## Quiero
registrar un paciente al ingreso a urgencias con detección de duplicados

## Para
evitar registros repetidos y capturar predictores clave del modelo (RF-001).

## Criterios de Aceptación
- [ ] CA1: Formulario captura ENT-001 completo, incluyendo ViaLlegada (catálogo Ambulancia/Particular/Remisión) y EpisodiosPreviosUrgencias.
- [ ] CA2: Antes del alta se busca duplicado por documento y por nombre/apellidos.
- [ ] CA3: Campos obligatorios no vacíos (RNQ-001); teléfono ≥10 dígitos aceptando +57; correo válido si no está vacío.
- [ ] CA4: Toda modificación queda registrada en ControlCambios.

## Recurso de datos involucrado
### Recurso
- **Nombre:** Paciente
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| TipoDoc, NumDoc | texto | Sí | Identificación |
| Nombres, Apellidos | texto | Sí | Buscables |
| Sexo, FechaNacimiento | catálogo/fecha | Sí | Demográficas |
| ViaLlegada | catálogo | Sí | Ambulancia / Particular / Remisión |
| EpisodiosPreviosUrgencias | entero | No | Predictor de alto peso |
| Teléfono, Correo | texto | Sí / No | +57 y formato @ |
| ContactoEmergencia + Teléfono | texto | Sí | Contacto |
| Departamento, Ciudad, Dirección | catálogo/texto | Sí | 32 deptos / ~200 ciudades |

### Relaciones con otros recursos
- `EventoTriaje` (1:N): un paciente tiene muchos eventos de triaje.
- `AntecedentesClinicos` (1:1): autorreporte si no hay HCE.

## Dependencias
E1 completo

## Subtareas
- [ ] Formulario en 4 secciones (datos, contacto, emergencia, residencia)
- [ ] Endpoint de búsqueda de duplicados
- [ ] Dropdowns Departamento → Ciudad dinámicos
