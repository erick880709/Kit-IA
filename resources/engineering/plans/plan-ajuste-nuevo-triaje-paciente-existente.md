# Plan — Ajuste: nuevo triaje para paciente existente (HU-E2-01)

**Fecha:** 2026-08-14
**Solicitud:** al registrar un paciente, validar con el número de documento si ya
existe; si existe, **precargar sus datos** para registrar su **nuevo triaje**.
Una persona puede tener N triajes porque son las veces que ha asistido a urgencias
(relación 1:N `Paciente → EventoTriaje`, ya modelada y probada en `test_historial_cronologico`).

**Criterio de aceptación:**
1. `Verificar documento` busca coincidencia EXACTA por tipo + número de documento.
2. Si existe → se precargan datos personales y de contacto, se muestra el número de
   triajes previos y la acción principal es **➕ Iniciar nuevo triaje**
   (`crear_evento` → pantalla `signos_vitales`), sin crear paciente duplicado.
3. Si no existe por documento → se conserva la búsqueda por nombre/apellidos (CA2
   original) y el alta normal.
4. Formulario vacío al verificar → no debe devolver "todos los pacientes" como
   duplicados (guard en servicio).

## Slices

| # | Slice | Archivos | Estado |
|---|-------|----------|--------|
| 1 | Servicio: `buscar_por_documento` + `datos_precarga` + guard de búsqueda vacía | `app/services/paciente_service.py`, `tests/test_paciente_service.py` | ✅ completado |
| 2 | Vista: flujo "existe → iniciar nuevo triaje" + limpieza de estado en sesión | `app/views/registro_paciente.py`, `app/main.py` | ✅ completado |

## Evidencia

- `resources/engineering/tests/coverage-paciente-service.md` (salida real de pytest).
- Verificación manual en navegador tras el despliegue (login → registro →
  documento existente → nuevo triaje).
