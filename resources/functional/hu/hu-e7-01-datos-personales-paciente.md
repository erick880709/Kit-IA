---
id: HU-E7-01
type: Historia de Usuario
epic: E7 - Datos Personales del Paciente
priority: High
points: 5
---

# HU-E7-01: Registrar datos personales completos del paciente

## Como
Enfermera / personal administrativo

## Quiero
registrar los datos personales completos del paciente (contacto y residencia)

## Para
cumplir el registro clínico y de contacto exigido por la institución (RF-001 extendido).

## Criterios de Aceptación
- [ ] CA1: Formulario completo en 4 secciones con validación por campo, incluyendo TipoSangre (catálogo A/B/AB/O + Rh) y Alergias (sustancia y tipo de alergia) como datos clínicos complementarios.
- [ ] CA2: Teléfono inválido o correo sin @ → error claro y sin guardado.
- [ ] CA3: Búsqueda por nombre encuentra pacientes con coincidencias parciales.
- [ ] CA4: Multi-visita con datos completos sin duplicar registros.
- [ ] CA5: `ControlCambios` registra cada modificación.
- [ ] CA6: Exportaciones anonimizan correo y teléfono (Ley 1581).

## Dependencias
TT-E7-01 + TT-E7-02 + TT-E7-03

## Subtareas
- [ ] Pruebas E2E del formulario completo
- [ ] Verificación de ControlCambios
