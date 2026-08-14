---
id: HU-03
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Alta
points: 5
---

# HU-03: Registro de paciente

## Como
Profesional de enfermería o médico

## Quiero
Registrar un nuevo paciente en el sistema con sus datos demográficos, documento, EPS, grupo sanguíneo y alergias, y poder buscar pacientes existentes por número de documento

## Para
Iniciar el proceso de triaje con los datos correctos del paciente y evitar duplicados

## Criterios de Aceptación

- [ ] CA1: La página tiene dos pestañas: "Nuevo Paciente" y "Buscar Paciente".
- [ ] CA2: **Pestaña Nuevo Paciente**: formulario con campos obligatorios marcados con asterisco (*):
  - Tipo de documento (select: CC, CE, TI, PA, RC)
  - Número de documento (input text)
  - Nombre (input text)
  - Apellido (input text)
  - Fecha de nacimiento (date picker)
  - Sexo (select: M, F)
  - Grupo sanguíneo (select: A+, A-, B+, B-, AB+, AB-, O+, O-)
  - EPS (select con 21 opciones de EPS_COLOMBIA)
  - Alergias (textarea, opcional)
  - Vía de llegada (select, default: Caminando)
  - Departamento (select, 32 departamentos)
  - Municipio (input text)
  - Teléfono (input text, validación formato colombiano)
  - Correo electrónico (input text, validación email)
- [ ] CA3: Validación en tiempo real: campos obligatorios muestran error si están vacíos al perder el foco. El documento se valida contra duplicados al presionar "Registrar".
- [ ] CA4: Si el documento ya existe, se muestra un panel de "Paciente Encontrado" con: nombre completo, edad, último triaje (fecha y nivel), total de episodios previos, y botón "Iniciar Nuevo Triaje".
- [ ] CA5: Si el documento no existe, se crea el paciente y se muestra confirmación con opción de "Iniciar Triaje".
- [ ] CA6: **Pestaña Buscar Paciente**: campo de búsqueda textual que busca por documento, nombre o apellido. Resultados en tabla con columnas: Documento, Nombre, Edad, EPS, Último Triaje.
- [ ] CA7: La edad se calcula automáticamente desde la fecha de nacimiento y se muestra en vivo.
- [ ] CA8: El formulario es responsive y usable en tablet.

## Recurso de datos involucrado

- **Nombre del recurso:** Paciente
- **Capa(s):** frontend (consume POST/GET /api/patients)

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| tipo_documento | select | Sí | Opciones: CC, CE, TI, PA, RC |
| numero_documento | string | Sí | Validación de duplicado en servidor → 409 |
| nombre | string | Sí | |
| apellido | string | Sí | |
| fecha_nacimiento | date | Sí | Calcula edad automáticamente |
| sexo | select | Sí | M / F |
| grupo_sanguineo | select | Sí | 8 opciones |
| alergias | textarea | No | Texto libre |
| eps | select | Sí | 21 opciones de EPS_COLOMBIA |
| via_llegada | select | No | Default: Caminando |
| departamento | select | No | 32 departamentos |
| municipio | string | No | |
| telefono | string | No | Formato colombiano |
| correo | string | No | Validación email |

### Relaciones con otros recursos
- `Triaje` (1:N): al registrar un paciente, se puede iniciar inmediatamente un triaje.

## Subtareas

- [ ] Crear `pages/PatientRegistrationPage.tsx` con tabs
- [ ] Crear formulario con React Hook Form + Zod (17 campos)
- [ ] Implementar validación en tiempo real
- [ ] Implementar detección de duplicados (409 → panel de paciente existente)
- [ ] Crear pestaña de búsqueda con debounced input
- [ ] Implementar cálculo de edad en vivo
- [ ] Estilos responsive
- [ ] Probar: registrar paciente nuevo, detectar duplicado, buscar paciente
