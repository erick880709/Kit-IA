---
id: TT-E7-02
type: Tarea Técnica
epic: E7 — Datos Ampliados del Paciente
priority: Alta
points: 3
---

# TT-E7-02: Actualizar PatientService con nuevos campos y validaciones

## Descripción
Modificar `PatientService.register_patient()` para aceptar y persistir los 9 campos nuevos. Agregar validaciones de formato para teléfono y correo. Actualizar `search_patients()` para incluir los nuevos campos en los resultados. Implementar búsqueda por nombre/apellidos además de por documento.

## Criterios de Done
- [ ] `register_patient()` acepta parámetros: nombres, apellidos, telefono, correo, contacto_emergencia, numero_contacto_emergencia, departamento, ciudad, direccion_residencia
- [ ] Validación de teléfono: debe tener al menos 10 dígitos, acepta +57 al inicio
- [ ] Validación de correo: si se proporciona, debe contener @ y .
- [ ] Validación de nombres/apellidos: mínimo 2 caracteres
- [ ] `search_patients()` incluye búsqueda por nombre y apellidos (LIKE %query%)
- [ ] `get_patient_by_document()` retorna todos los campos nuevos
- [ ] `get_patient_triage_history()` incluye nombres y apellidos en el resultado
- [ ] Cada actualización de estos campos registra entrada en `ControlCambios`

## Dependencias
- TT-E7-01 (Extender schema BD) — debe ejecutarse primero

## Subtareas
- [ ] Agregar parámetros a register_patient()
- [ ] Implementar _validar_telefono() y _validar_correo()
- [ ] Actualizar INSERT para incluir nuevos campos
- [ ] Actualizar search_patients() con búsqueda por nombre
- [ ] Integrar registrar_cambio() en cada modificación
