---
id: TT-E7-03
type: Tarea Técnica
epic: E7 — Datos Ampliados del Paciente
priority: Alta
points: 5
---

# TT-E7-03: Actualizar UI de registro de paciente con nuevos campos

## Descripción
Modificar `patient_page.py` para agregar los 9 campos nuevos al formulario de registro de paciente (P02). Organizar el layout en secciones lógicas: Datos Personales, Contacto, Contacto de Emergencia, Residencia. Implementar dropdowns para departamento y ciudad con dependencia (al seleccionar departamento, se filtran las ciudades).

## Criterios de Done
- [ ] Nueva sección "Datos Personales": Nombres*, Apellidos* (antes de Tipo Documento)
- [ ] Nueva sección "Contacto": Teléfono*, Correo
- [ ] Nueva sección "Contacto de Emergencia": Nombre*, Teléfono*
- [ ] Nueva sección "Residencia":
  - **Departamento***: dropdown de selección única con los 32 departamentos de Colombia (catálogo `DEPARTAMENTOS_COLOMBIA`)
  - **Ciudad***: dropdown **dependiente** que se actualiza automáticamente al seleccionar departamento — solo muestra las ciudades del departamento elegido (`CIUDADES_POR_DEPARTAMENTO[depto]`)
  - **Dirección***: campo de texto libre
- [ ] Mecanismo de dropdown dependiente:
  ```python
  depto = st.selectbox("Departamento *", options=DEPARTAMENTOS_COLOMBIA)
  ciudades_disponibles = CIUDADES_POR_DEPARTAMENTO.get(depto, [])
  ciudad = st.selectbox("Ciudad *", options=ciudades_disponibles)
  ```
- [ ] Validación visual: campos obligatorios con indicador *, borde rojo si vacíos
- [ ] Teléfono: placeholder "3001234567", validación de formato al perder foco
- [ ] Correo: placeholder "paciente@email.com", validación de formato
- [ ] Layout responsive: en pantallas anchas usa 2 columnas, en móviles 1 columna
- [ ] Al editar un paciente existente (flujo duplicado), los nuevos campos se precargan incluyendo departamento y ciudad
- [ ] Tooltip o help text en cada campo explicando el formato esperado

## Dependencias
- TT-E7-01 (Schema BD)
- TT-E7-02 (PatientService actualizado)

## Subtareas
- [ ] Rediseñar layout del formulario con 4 secciones
- [ ] Implementar dropdowns encadenados Departamento → Ciudad
- [ ] Agregar validación client-side para teléfono y correo
- [ ] Actualizar flujo de duplicados para mostrar nuevos campos
- [ ] Probar flujo completo: registro → búsqueda → historial con nuevos datos
