# 4. Desarrollo de la contribución — TriajeIA (hechos consumados)

> Tiempo verbal: pretérito (trabajo ya ejecutado). Fuentes: `resources/architecture/`,
> `triaje-ia/` (código versionado en `erick880709/Kit-IA`, rama `main`), ADR-001..004.

## 4.1 Arquitectura implementada

Se implementó un **monolito modular** sobre Streamlit (Python 3.12) con
SQLAlchemy 2.0 y SQLite (ADR-002), organizado en cuatro capas estrictas:
`views` (presentación), `services` (lógica de negocio), `domain` (entidades y
catálogos) y `infra` (persistencia, configuración, logging). La interfaz de
usuario constó de 8 pantallas clínicas más 5 pantallas administrativas
(roles, comparación de modelos, auditoría, dashboard y gestión de modelos).

## 4.2 Funcionalidad clínica (Épicas E1–E2)

- **Autenticación y RBAC:** login con bcrypt y bloqueo por 5 intentos, cuatro
  roles (médico, enfermería, auditor, investigador), recuperación de contraseña
  con token de 15 minutos almacenado como hash SHA-256 (un solo uso) y cierre
  por inactividad de 5 minutos, todo auditado.
- **Flujo de triaje:** registro de pacientes con detección de duplicados
  (documento + nombre), búsqueda, historial, captura de signos vitales con
  rangos de plausibilidad y confirmación explícita fuera de rango, evaluación
  clínica (escala de dolor, Glasgow), máquina de 7 estados del evento de
  triaje, reclasificación y cierre con informe PDF anonimizado (iniciales y
  máscara de documento, Res. 5596/2015 y Ley 1581/2012).

## 4.3 Motor de IA y pipeline de entrenamiento (Épicas E3–E4)

El pipeline reproducible (`ml/pipeline.py`, 10 pasos, semilla 42) ejecutó:
generación del demo sintético calibrado con la distribución real medida del
dataset nacional MinSalud (89.453 eventos; I 0.23 %, II 3.03 %, III 88.54 %,
IV 7.75 %, V 0.46 %) → anonimización → limpieza → features estructuradas +
TF-IDF sobre CIE-10 y texto libre → split estratificado 70/15/15 **antes** del
feature engineering (escalador e imputador ajustados solo con train — diseño
anti-fuga) → baselines (regresión logística, random forest, XGBoost con CV
estratificado y pesos balanceados) → fusión temprana vs. tardía → afinado del
ganador (búsqueda en rejilla `max_depth ∈ {3,5}`, `learning_rate ∈ {0.05,0.1}`
con validación) → submodelo de texto entrenado adicionalmente con la cohorte
real de San Juan de Dios (43.594 eventos) → peso del combinador elegido por
validación (0.5) → umbrales por clase optimizados con índice de Youden
priorizando recall en niveles I–II → SHAP → serialización versionada con
manifiesto y hash sha256 verificado **antes** de la deserialización (CWE-502).

En la aplicación, el servicio de inferencia cargó el artefacto activo según la
base de datos (con invalidación de caché ante cambios), ejecutó la predicción
en un ejecutor con timeout de 3 segundos y fallback manual (RNF-007), e incluyó
la explicación SHAP top-5 en lenguaje clínico dentro del presupuesto de tiempo.

## 4.4 Auditoría, dashboard y gestión de modelos (Épicas E5–E6)

- **Auditoría append-only:** protección a nivel ORM contra actualización y
  borrado, registro de cambios y clasificaciones IA en la misma transacción
  (`registrar(commit=False)` + commit único), consulta con filtros y
  exportación CSV/Excel/PDF.
- **Dashboard operativo:** 7 indicadores con semáforo contra las metas RNF-001.
- **Gestión de modelos:** registro, activación/desactivación con protección del
  último modelo activo, historial de activaciones e integración con la recarga
  del singleton de inferencia.

## 4.5 Calidad y seguridad verificadas (evidencia de procesos)

El entregable pasó por revisión de código de cinco ejes (3 hallazgos
bloqueantes y 17 correcciones resueltos — `resources/engineering/reviews/review-e1-e6.md`),
auditoría OWASP con un hallazgo bloqueante CWE-502 resuelto y 12 hallazgos
documentados (`resources/engineering/security/hardening-triaje-ia.md`), y
103 pruebas automatizadas en verde con análisis estático sin errores
(`ruff`), reproducidas en un pipeline de integración continua
(`.github/workflows/ci.yml`).
