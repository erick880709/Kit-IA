# TriajeIA — Demo de Triaje Multimodal IA (TFM UNIR)

> Generado por `genesis` a partir de `resources/architecture/Documento_Arquitectura_TriajeIA.md` — `builder` debe actualizar este proyecto incrementalmente, no regenerarlo desde cero.

Monolito modular **Streamlit** (Python 3.12) para el flujo clínico de triaje de 8 pantallas + pipeline de entrenamiento offline. Sistema de **apoyo a la decisión** (no autónomo): la IA sugiere nivel I–V (Res. 5596/2015) con probabilidades y explicación SHAP; el profesional valida y decide.

## Estructura

```
triaje-ia/
├── app/
│   ├── main.py            # Punto de entrada Streamlit (bootstrap + plomería)
│   ├── views/             # Pantallas (builder genera una por HU)
│   ├── domain/            # Entidades y reglas puras (sin Streamlit)
│   ├── services/          # Inferencia, NLP, SHAP (builder)
│   └── infra/             # Config, BD, logging, errores, auth
├── ml/                    # Pipeline de entrenamiento offline (Épica E3)
│   ├── configs/features.yaml
│   ├── data/{raw,processed}/
│   ├── notebooks/
│   ├── src/{data,features,models,evaluation}/
│   └── pipeline.py        # orquestador: demo→ingesta→anonimización→…→artefacto
├── scripts/healthcheck.py # Verificación end-to-end de plomería
├── tests/                 # pytest
├── artifacts/
│   ├── models/            # Modelos versionados (joblib + manifiesto con hash)
│   ├── metrics/           # Métricas por experimento (JSON)
│   └── shap/              # Explicaciones agregadas
└── requirements.txt
```

## Requisitos

- Python 3.12+ (probado con 3.11/3.12)
- `pip` y `venv`

## Puesta en marcha local

```bash
cd triaje-ia
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt -r requirements-dev.txt
copy .env.example .env          # ajustar valores si se desea
python scripts/healthcheck.py   # debe salir TODO OK
pytest                          # test de salud
streamlit run app/main.py
```

## Variables de entorno

Ver `.env.example`. Secretos nunca en código: `APP_SECRET_KEY`, `DB_PATH`.

## Seguridad (TT-E1-03)

- **Transporte (demo local):** la demo corre en `http://localhost`. Opcional para exposiciones:
  HTTPS con certificado self-signed local:
  `streamlit run app/main.py --server.sslCertFile cert.pem --server.sslKeyFile key.pem`
  (generar con `openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 30 -nodes`).
- **Contraseñas:** hash bcrypt con salt aleatorio — nunca texto plano (HU-E1-01 CA2).
- **Cifrado en reposo:** la demo usa SQLite con datos sintéticos; para producción el diseño previsto
  es cifrado a nivel de disco/BD + TLS (documentado en el ADR del documento de arquitectura).
- **Sin secretos hardcodeados:** toda configuración sensible vive en `.env` (no versionado).

## Extensión HCE (TT-E1-04)

`app/services/history_connector.py` define el puerto `HistoryConnector` con la implementación
`MockHCE` (autorreporte local). Para integrar una Historia Clínica Electrónica real, se
implementa un nuevo `HistoryConnector` y se reemplaza la instancia en ese módulo — sin tocar
el resto del sistema. Inyección simple de dependencias documentada: la UI nunca accede a SQL
(servicios → ORM), separación UI / lógica / persistencia por capas (`views / services / domain / infra`).

## Entrenamiento del modelo (Épica E3)

```bash
python -m ml.pipeline --n 4000 --k-folds 5
```

El orquestador ejecuta de punta a punta: demo sintético calibrado con la distribución
real **medida** en el dataset nacional MinSalud (89.453 eventos, `datasets/`) → anonimización
obligatoria (Ley 1581/2012) → limpieza → features estructuradas + TF-IDF (CIE-10 + texto) →
split 70/15/15 estratificado → baselines (CV, class weights) → early vs late fusion →
**fusión tardía afinada**: XGBoost estructurado (búsqueda de hiperparámetros + pesos
balanceados) + Regresión Logística sobre CIE+texto entrenada con la **cohorte real del
Hospital San Juan de Dios** (43.594 eventos, fine-tuning colombiano) → peso del combinador
elegido por validación → umbrales por clase (recall I-II) → SHAP top-5 → benchmarks →
serialización versionada con manifiesto y hash.

**Resultados actuales (split anti-fuga):** AUC-ROC 0.968 (supera CTAS 0.882 / Hong 0.93 /
Ueareekul 0.917), macro-F1 0.551. ⚠ Limitación documentada: el demo sintético genera el
CIE-10 condicionado al nivel, por lo que el AUC sobre demo-test es optimista; la evidencia
honesta del submodelo de texto real está en `artifacts/metrics/texto_sjd_holdout.json`
(holdout SJdD sin fuga, F1 ≈ 0.09). Las metas RNF-001 se verificarán con MIMIC-IV-ED
(credenciales PhysioNet pendientes).

## Validación científica (paso 2 post-desarrollo)

```bash
python -m ml.validacion --n 4000
```

Auditoría de 7 fases sobre el artefacto ganador: fuga de datos, CV estratificada, McNemar +
IC bootstrap 1000, calibración (Brier/ECE), equidad por subgrupo, trazabilidad y model card.
Resultados en `resources/tfm/validacion-cientifica/` (reporte + model card + respaldo JSON).

**Inferencia en la app:** `app/services/inference_service.py` carga el artefacto al primer
uso, registra el modelo en BD (ENT-009), predice con presupuesto < 3 s y fallback a triaje
manual auditado si el modelo no responde (RNF-009/RNO-007). La explicación SHAP por evento
se muestra en la pantalla "Explicación de la clasificación IA" (lenguaje clínico, dirección
del efecto y alerta de signos prioritarios MTS).

## Estado del scaffold

- **Épica E1 completa (4/4):** HU-E1-01 login bcrypt + bloqueo 5 intentos · HU-E1-02 RBAC por pantalla
  (13 pantallas × roles) + gestión de roles auditada · HU-E1-03 recuperación con token 15 min ·
  HU-E1-04 cierre por inactividad 5 min auditado. TT-E1-03 (TLS doc) y TT-E1-04 (modular + HistoryConnector).
- **Épica E2 completa (8/8):** HU-E2-01 registro con precarga de duplicados · HU-E2-02 búsqueda paginada ·
  HU-E2-03 historial · HU-E2-04 signos vitales con rangos y alertas · HU-E2-05 evaluación clínica
  (doble captura + autorreporte) · HU-E2-06 máquina de 7 estados auditada · HU-E2-07 reclasificación
  como evento separado · HU-E2-08 cierre con concordancia + PDF descargable.
- **Épica E3 completa (9/9 TT):** ingesta 5 fuentes + anonimización (TT-E3-01) · limpieza (TT-E3-02) ·
  embeddings TF-IDF con fallback BERT documentado (TT-E3-03) · baselines CV (TT-E3-04) · early fusion
  (TT-E3-05) · late fusion (TT-E3-06) · umbrales por clase recall I-II (TT-E3-07) · SHAP + benchmarks
  (TT-E3-08) · serialización versionada con hash (TT-E3-09). **Datos reales integrados:** SJdD
  (43.594 eventos) entrena el submodelo de texto; MinSalud nacional (89.453) calibra la distribución.
- **Épica E4 completa (4 HU + 1 TT):** HU-E4-01 inferencia real < 3 s con probabilidades, umbrales
  y metadatos · HU-E4-02 explicación SHAP en lenguaje clínico con export · HU-E4-03 validación
  sin nivel preseleccionado · HU-E4-04 comparación de modelos vs literatura (rol Investigador).
  TT-E4-01: carga con log de versión, circuit breaker, fallback manual y registro ENT-009.
- **Épica E5 completa (2 HU + 1 TT):** TT-E5-01 auditoría append-only (UPDATE/DELETE bloqueados
  a nivel ORM) + decorador `@auditar` + inferencias con versión/umbrales/confianza (RNA-010).
  HU-E5-01 consulta y exportación de auditoría con filtros (fecha/usuario/entidad/acción/evento),
  paginada < 1 s y export CSV/Excel/PDF (rol Auditor/Administrador). HU-E5-02 registro de triaje
  descargable en PDF normativo (Res. 5596/2015): paciente seudonimizado sin identificadores
  directos, niveles IA vs humano, signos, motivo y variables SHAP — generación auditada.
- **Épica E6 completa (3 HU):** HU-E6-02 gestión de modelos: registro versionado (CA1),
  activación y rollback con un clic (CA2) — la inferencia usa la versión activa en BD —,
  historial de activaciones auditado (CA3) y RBAC Administrador/Investigador (CA4).
  HU-E6-01 dashboard operativo en vivo: 7 indicadores (distribución por nivel, tiempo promedio,
  desempeño IA, concordancia global y por nivel, volumen), semáforo de metas RNF-001 (CA2),
  matriz de confusión IA vs profesional y discrepancias filtrables (CA3). HU-E6-03 exportación
  de reportes Excel/PDF/CSV anonimizada y auditada.
- Semilla demo: `python scripts/seed_demo.py` (roles + 5 usuarios, contraseña `Demo123!`).
- **Épicas E1–E6 completas** y aprobadas en revisión de 5 ejes (Centinela): reporte en
  `resources/engineering/reviews/review-e1-e6.md` con todas las resoluciones.
  Pendiente de datos: MIMIC-IV-ED (credenciales PhysioNet) y RIPS.
