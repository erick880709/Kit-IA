---
id: HU-E8-06
type: Historia de Usuario
epic: E8-Gestión-Usuarios
priority: Alta
points: 2
---

# HU-E8-06: Sistema bloquea nuevo triaje si el paciente tiene uno activo

## Como
Enfermera / Médico

## Quiero
Que el sistema me impida crear un nuevo triaje para un paciente que ya tiene uno en curso (no cerrado ni cancelado)

## Para
Evitar duplicidad de episodios y mantener la integridad del flujo clínico

## Criterios de Aceptación
- [ ] CA1: Al intentar registrar un paciente que ya tiene un triaje activo (estado ≠ Cerrado/Cancelado), se muestra un mensaje de advertencia
- [ ] CA2: El mensaje indica: "⚠️ Este paciente tiene un triaje en curso (Estado: [estado]). Debe cerrarlo o cancelarlo antes de crear uno nuevo."
- [ ] CA3: Se muestra el ID del triaje activo como enlace para navegar directamente a él
- [ ] CA4: Si el paciente NO tiene triajes activos, el flujo de creación de triaje procede normalmente
- [ ] CA5: Esta validación aplica tanto en "Nuevo Paciente" como en "Buscar Paciente" (botón "Nuevo Triaje")

## Subtareas
- [ ] Modificar `_render_new_patient_form()` en `patient_page.py` para verificar triajes activos antes de crear
- [ ] Modificar `_render_patient_card()` para deshabilitar/ocultar botón "Nuevo Triaje" si hay uno activo
- [ ] Usar `TriageService.get_active_triage_for_patient()` para la verificación
- [ ] Mostrar badge con el estado actual del triaje activo en la interfaz
- [ ] Agregar enlace clickable al triaje activo para navegar directamente a él
