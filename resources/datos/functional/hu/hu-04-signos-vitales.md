---
id: HU-04
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Alta
points: 5
---

# HU-04: Captura de signos vitales

## Como
Profesional de enfermería

## Quiero
Registrar los signos vitales del paciente (frecuencia cardíaca, respiratoria, presión arterial, temperatura, saturación de oxígeno) y ver alertas visuales si algún valor está fuera del rango fisiológico normal

## Para
Obtener una primera evaluación objetiva del estado del paciente que alimente al modelo de IA

## Criterios de Aceptación

- [ ] CA1: La página verifica que hay un triaje activo. Si no, muestra mensaje "No hay un triaje activo" con botón para ir a Registrar Paciente.
- [ ] CA2: Se muestra un expander "Buscar Paciente" (componente `PatientSearch` reutilizable) que permite localizar al paciente por documento y ver sus datos básicos.
- [ ] CA3: Formulario con 6 campos numéricos obligatorios:
  - Frecuencia Cardíaca (FC) — lpm, rango normal 60-100
  - Frecuencia Respiratoria (FR) — rpm, rango normal 12-20
  - Presión Arterial Sistólica (TA S) — mmHg, rango normal 90-140
  - Presión Arterial Diastólica (TA D) — mmHg, rango normal 60-90
  - Temperatura (Tº) — °C, rango normal 36.0-37.5
  - Saturación de Oxígeno (SpO2) — %, rango normal 95-100
- [ ] CA4: Al ingresar un valor, se muestra **en tiempo real** (sin esperar a submit):
  - 🟢 Verde si está en rango normal.
  - 🟡 Amarillo con warning si está en rango límite.
  - 🔴 Rojo con alerta si está en rango crítico.
- [ ] CA5: Se calcula y muestra automáticamente el IMC si el paciente tiene talla y peso registrados.
- [ ] CA6: Al presionar "Guardar Signos Vitales", se envía `PUT /api/triages/{id}/vital-signs` y se muestran las alertas generadas por el servidor (si las hay).
- [ ] CA7: Navegación al siguiente paso: botón "Continuar a Evaluación Clínica".
- [ ] CA8: La página previene navegación accidental si hay cambios sin guardar (dirty state).

## Recurso de datos involucrado

- **Nombre del recurso:** SignosVitales
- **Capa(s):** frontend (consume PUT/GET /api/triages/{id}/vital-signs)

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| frecuencia_cardiaca | number | Sí | 30-250 lpm |
| frecuencia_respiratoria | number | Sí | 5-60 rpm |
| presion_sistolica | number | Sí | 40-280 mmHg |
| presion_diastolica | number | Sí | 20-180 mmHg |
| temperatura | number | Sí | 30.0-45.0 °C |
| saturacion_oxigeno | number | Sí | 30-100 % |
| imc | number | No | Calculado si hay talla/peso |

## Subtareas

- [ ] Crear `pages/VitalSignsPage.tsx`
- [ ] Crear `components/clinical/PatientSearch.tsx` (reutilizable)
- [ ] Crear `components/clinical/VitalSignsForm.tsx` con validación de rangos
- [ ] Implementar alertas visuales en tiempo real (verde/amarillo/rojo)
- [ ] Implementar cálculo de IMC automático
- [ ] Implementar dirty state guard
- [ ] Probar con valores normales, límite y críticos
