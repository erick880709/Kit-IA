# Resumen / Abstract — TriajeIA (versión para depósito)

> Redactado por `tfm-redactor` con cifras verificadas contra `triaje-ia/artifacts/metrics/`.
> Ninguna cifra de este resumen se escribió sin su archivo fuente.

## Resumen (español)

El triaje de urgencias en Colombia se realiza según la Resolución 5596 de 2015
(niveles I–V), y su calidad depende de la disponibilidad y experiencia del
profesional. Este trabajo desarrolló **TriajeIA**, un sistema de apoyo a la
decisión clínica basado en inteligencia artificial multimodal que integra
signos vitales estructurados y texto clínico libre (motivo de consulta y código
CIE-10). Se implementó una arquitectura monolítica modular (Streamlit,
SQLAlchemy, SQLite) con control de acceso por roles, auditoría de trazabilidad
inmutable y explicabilidad con SHAP, cumpliendo los principios de privacidad de
la Ley 1581 de 2012.

El motor de IA combina, mediante **fusión tardía ponderada**, un clasificador
XGBoost sobre variables estructuradas (hiperparámetros afinados por búsqueda en
rejilla con validación, pesos balanceados por clase) y una regresión logística
sobre representaciones TF-IDF del texto clínico, entrenada con una cohorte real
de 43.594 eventos de urgencias (Hospital San Juan de Dios). El diseño
experimental aplicó split estratificado 70/15/15 con semilla fija, ajustando
todos los preprocesadores únicamente sobre el conjunto de entrenamiento
(verificación anti-fuga) y umbrales de decisión por clase que priorizan la
sensibilidad en los niveles críticos I y II.

Sobre el conjunto de prueba del dataset sintético de demostración (calibrado
con la distribución nacional medida en 89.453 eventos reales), el modelo
alcanzó una **exactitud de 0.978, AUC-ROC macro de 0.968 y macro-F1 de 0.551**;
la prueba de McNemar confirmó que supera significativamente a la regla
mayoritaria (p ≈ 0). La calibración resultó adecuada (Brier 0.036; ECE 0.042).
Los niveles clínicamente prioritarios obtuvieron en el conjunto de prueba un
recall de 0.812 (nivel II) con precisión de 0.867. Estos resultados, si bien
favorables, deben interpretarse como **evidencia preliminar**: el CIE-10
sintético está condicionado al nivel de triaje, y la evaluación honesta del
submodelo de texto sobre la cohorte real SJdD arroja una macro-F1 de 0.088,
por lo que la validación definitiva queda supeditada a un conjunto externo
(MIMIC-IV-ED) y a la autorización del Comité de Ética.

**Palabras clave:** triaje hospitalario, inteligencia artificial, fusión
tardía, XGBoost, SHAP, urgencias, Colombia.

## Abstract (English)

This work developed **TriajeIA**, a clinical decision-support system that
combines structured vital signs and free clinical text (chief complaint and
ICD-10 code) through a weighted **late fusion** of an XGBoost classifier and a
logistic regression over TF-IDF text features, the latter trained on a real
cohort of 43,594 emergency events from a Colombian hospital. A stratified
70/15/15 split with fixed seed, train-only preprocessing (leakage-verified
design) and per-class decision thresholds prioritizing recall on critical
levels I–II were applied. On the synthetic demonstration test set, the model
achieved **accuracy 0.978, macro AUC-ROC 0.968 and macro-F1 0.551**, with
McNemar's test confirming significant superiority over the majority-class rule
(p ≈ 0) and adequate calibration (Brier 0.036; ECE 0.042). Level II reached
recall 0.812 with precision 0.867. Results are declared as **preliminary
evidence**: the synthetic ICD-10 codes are conditioned on the triage level,
and the honest holdout evaluation of the text submodel on the real cohort
yields macro-F1 0.088; definitive external validation (MIMIC-IV-ED) and
institutional ethics approval remain pending.

**Keywords:** hospital triage, artificial intelligence, late fusion, XGBoost,
SHAP, emergency department, Colombia.
