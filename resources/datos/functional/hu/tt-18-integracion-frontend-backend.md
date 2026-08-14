---
id: TT-18
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 5
dependencies: "TT-08, TT-09, TT-10, TT-11, TT-12, TT-13, HU-01 a HU-14"
---

# TT-18: Integración frontend ↔ backend

## Descripción

Conectar todos los hooks de TanStack Query y las llamadas a la API del frontend React con los endpoints de FastAPI. Verificar que el flujo completo de triaje funciona de extremo a extremo. Resolver problemas de CORS, manejo de errores y estados de carga.

## Criterios de Done

- [ ] Todos los archivos en `api/*.ts` están implementados y tipados correctamente con las respuestas de la API.
- [ ] Los hooks en `hooks/*.ts` usan TanStack Query con las configuraciones adecuadas (`staleTime`, `retry`, `onError`).
- [ ] **Flujo completo de triaje** probado manualmente:
  1. Login → JWT almacenado
  2. Registrar paciente → POST /api/patients
  3. Crear triaje → POST /api/triages
  4. Guardar signos vitales → PUT /api/triages/{id}/vital-signs
  5. Guardar evaluación clínica → PUT /api/triages/{id}/clinical-eval
  6. Clasificación IA → POST /api/inference/predict (con spinner)
  7. Explicación SHAP → POST /api/inference/explain
  8. Cerrar triaje → POST /api/triages/{id}/close
  9. Descargar informe → GET /api/reports/triage/{id}/download
- [ ] **Dashboard** carga KPIs correctamente.
- [ ] **Gestión de modelos** muestra modelos reales del disco.
- [ ] **Auditoría** muestra registros con filtros funcionales.
- [ ] **Gestión de usuarios** permite CRUD completo.
- [ ] Manejo de errores: errores de red, 401 (redirigir a login), 404, 409, 422, 500 se muestran con mensajes amigables.
- [ ] CORS funciona tanto en desarrollo (Vite proxy) como con el backend directo.

## Recurso de datos involucrado

No aplica — es integración de sistemas.

## Subtareas

- [ ] Implementar todos los archivos `api/*.ts`
- [ ] Implementar todos los hooks `hooks/*.ts`
- [ ] Probar flujo completo de triaje (end-to-end manual)
- [ ] Probar dashboard con datos reales
- [ ] Probar gestión de modelos
- [ ] Probar auditoría con filtros
- [ ] Probar gestión de usuarios CRUD
- [ ] Manejo de errores global
- [ ] Verificar CORS en desarrollo y producción
