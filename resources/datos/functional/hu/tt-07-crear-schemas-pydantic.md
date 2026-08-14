---
id: TT-07
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 5
dependencies: "TT-06"
---

# TT-07: Crear schemas Pydantic para request/response

## Descripción

Definir todos los modelos Pydantic que usará la API REST para validar requests y serializar responses. Esto incluye schemas para autenticación, pacientes, triajes, signos vitales, evaluación clínica, inferencia, dashboard, modelos, auditoría, reportes, usuarios y control de cambios.

## Criterios de Done

- [ ] Archivos creados en `schemas/`:
  - `auth.py`: `LoginRequest`, `LoginResponse`, `TokenData`, `ResetTokenRequest`, `ResetPasswordRequest`
  - `patient.py`: `PatientCreate`, `PatientResponse`, `PatientSearchResult`
  - `triage.py`: `TriageCreate`, `TriageResponse`, `VitalSignsUpdate`, `ClinicalEvalUpdate`, `StateTransition`, `ReclassifyRequest`, `CloseRequest`
  - `inference.py`: `PredictRequest`, `PredictResponse`, `ExplainResponse`, `InferenceStatus`
  - `dashboard.py`: `DashboardKpisResponse`, `Triages7dResponse`
  - `models.py`: `ModelResponse`, `ModelRegisterRequest`, `ModelScanResult`
  - `audit.py`: `AuditQueryParams`, `AuditEntryResponse`
  - `reports.py`: `ReportResponse`
  - `users.py`: `UserCreate`, `UserUpdate`, `UserResponse`
  - `common.py`: `GenericApiResponse[T]`, `PaginatedResponse[T]`, `ErrorResponse`
- [ ] Schemas usan tipos Python nativos (str, int, float, bool, Optional, List, Dict).
- [ ] Campos obligatorios usan `...` (Ellipsis); opcionales usan `Optional[T]` con default.
- [ ] Validaciones básicas con `Field()`: longitudes mín/máx, rangos numéricos, regex para documento/teléfono.
- [ ] Los schemas reflejan exactamente los campos que los servicios esperan/devuelven.
- [ ] Los schemas son compatibles con los catálogos existentes (constantes Python).

## Recurso de datos involucrado

Esta tarea define el contrato de datos para TODOS los recursos del sistema. Cada schema está mapeado a la entidad correspondiente del modelo de dominio (RD-002).

## Subtareas

- [ ] Crear `schemas/common.py` con tipos genéricos
- [ ] Crear `schemas/auth.py`
- [ ] Crear `schemas/patient.py`
- [ ] Crear `schemas/triage.py`
- [ ] Crear `schemas/inference.py`
- [ ] Crear `schemas/dashboard.py` + `schemas/models.py`
- [ ] Crear `schemas/audit.py` + `schemas/reports.py` + `schemas/users.py`
- [ ] Validar schemas contra servicios existentes
