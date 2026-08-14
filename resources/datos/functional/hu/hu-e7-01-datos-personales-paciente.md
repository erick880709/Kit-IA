---
id: HU-E7-01
type: Historia de Usuario
epic: E7 — Datos Ampliados del Paciente
priority: Alta
points: 5
---

# HU-E7-01: Registrar datos personales completos del paciente

## Como
Personal Administrativo / Enfermera de Triaje

## Quiero
Registrar nombres, apellidos, teléfono, correo (opcional), contacto de emergencia, número de contacto de emergencia, departamento, ciudad y dirección de residencia del paciente

## Para
Cumplir con la normativa colombiana de historia clínica (Res. 1995/1999), permitir contacto con el paciente o su familiar en caso de emergencia, y tener trazabilidad completa de la atención.

## Criterios de Aceptación
- [ ] CA1: El formulario de registro de paciente muestra los campos Nombres*, Apellidos*, Teléfono*, Correo, ContactoEmergencia*, NúmContactoEmergencia*, Departamento*, Ciudad*, Dirección*
- [ ] CA2: Los campos obligatorios (*) muestran validación visual (borde rojo) si se intenta guardar sin completarlos
- [ ] CA3: El correo electrónico se valida con formato básico (contiene @ y .)
- [ ] CA4: Los números de teléfono aceptan formato colombiano (10 dígitos, puede incluir +57)
- [ ] CA5: El campo **Departamento** es una lista desplegable de selección única con los 32 departamentos de Colombia. El campo **Ciudad** es una **lista dependiente**: al seleccionar un departamento, solo se muestran las ciudades que pertenecen a ese departamento (catálogo `CIUDADES_POR_DEPARTAMENTO`).
- [ ] CA6: Al guardar, todos los campos nuevos se persisten en la tabla Paciente
- [ ] CA7: Cada modificación de estos campos queda registrada en ControlCambios con usuario, fecha y motivo

## Recurso de datos involucrado

### Recurso
- **Nombre:** Paciente (extensión)
- **Capa(s):** backend + frontend

### Campos del recurso (nuevos)
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| Nombres | TEXT | Sí | Nombres del paciente. Mínimo 2 caracteres. |
| Apellidos | TEXT | Sí | Apellidos del paciente. Mínimo 2 caracteres. |
| Telefono | TEXT | Sí | Número de teléfono. Formato: 10 dígitos, acepta +57. |
| Correo | TEXT | No | Correo electrónico. Validación básica de formato. |
| ContactoEmergencia | TEXT | Sí | Nombre completo del contacto de emergencia. |
| NumeroContactoEmergencia | TEXT | Sí | Teléfono del contacto de emergencia. Formato igual a Teléfono. |
| Departamento | TEXT | Sí | Departamento de residencia. Catálogo controlado (32 deptos). |
| Ciudad | TEXT | Sí | Ciudad/municipio de residencia. Catálogo controlado. |
| DireccionResidencia | TEXT | Sí | Dirección completa de residencia. |

## Subtareas
- [ ] Agregar columnas a la tabla Paciente en database.py
- [ ] Crear catálogo de departamentos y ciudades de Colombia
- [ ] Actualizar PatientService.register_patient() con nuevos campos
- [ ] Actualizar formulario UI en patient_page.py
- [ ] Agregar validación de formato para teléfono y correo
