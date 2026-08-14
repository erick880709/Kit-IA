# RF-PAC-004: Validación de Datos del Paciente

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 40, Módulo de Gestión del Paciente
**Prioridad:** Alta

## Descripción
El sistema verificará automáticamente la integridad y consistencia de los datos del paciente al momento del registro, detectando duplicados, validando formatos y asegurando que todos los campos obligatorios estén completos.

## Actores involucrados
- Sistema (automático)
- Personal Administrativo (recibe alertas de validación)

## Criterios de aceptación
- Detección de pacientes duplicados por número de documento antes de crear un nuevo registro.
- Validación de formatos: tipo de documento (catálogo), número de documento (alfanumérico), fecha de nacimiento (formato fecha).
- Verificación de campos obligatorios: tipo de documento, número de documento, fecha de nacimiento, sexo.
- Alertas visuales en campos con error de formato o vacíos obligatorios.
- Prevención de envío del formulario hasta que todos los campos obligatorios sean válidos.

## Dependencias / relacionados
- RF-PAC-001: Registrar Paciente.
- RNQ-001: Campos obligatorios no vacíos.
- RNQ-005: No se permiten formatos ambiguos de fecha y hora.
- RNQ-006: Identificación de registros duplicados.

## Notas del analista
- La validación de duplicados debe ejecutarse en tiempo real (al perder el foco del campo de documento) para evitar que el usuario complete todo el formulario antes de descubrir que el paciente ya existe.
