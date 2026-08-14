---
id: HU-E8-05
type: Historia de Usuario
epic: E8-Gestión-Usuarios
priority: Media
points: 3
---

# HU-E8-05: Administrador consulta historial de cambios (Control de Cambios)

## Como
Administrador

## Quiero
Ver un registro de todas las modificaciones hechas sobre pacientes, triajes y signos vitales

## Para
Auditar quién cambió qué dato clínico y cuándo

## Criterios de Aceptación
- [ ] CA1: La página "Control de Cambios" solo es accesible para el rol Administrador
- [ ] CA2: Se muestra una tabla con: Fecha/Hora, Usuario, Entidad, Campo Modificado, Valor Anterior → Valor Nuevo, Documento Paciente
- [ ] CA3: Se puede filtrar por: Entidad (Paciente/EventoTriaje/SignosVitales), Usuario, Número de Documento, Rango de fechas
- [ ] CA4: Los resultados se ordenan del más reciente al más antiguo
- [ ] CA5: Se muestra el total de cambios encontrados
- [ ] CA6: El administrador puede exportar los resultados a CSV

## Subtareas
- [ ] Crear `control_cambios_page.py` con tabla de historial
- [ ] Implementar filtros: `st.selectbox` para Entidad, `st.text_input` para Usuario y Documento, `st.date_input` para rango de fechas
- [ ] Usar `PatientService.get_historial_cambios()` para obtener datos
- [ ] Agregar paginación (20 resultados por página)
- [ ] Implementar exportación CSV con `st.download_button` y `pd.DataFrame.to_csv()`
