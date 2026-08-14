# Plantilla — Model Card

> Basada en el formato estándar de Mitchell et al. (2019), "Model Cards for Model Reporting",
> adaptado al alcance de este TFM. Un archivo por modelo candidato relevante (al menos el
> ganador); opcionalmente uno por cada baseline para la comparación del Cap. 5.

```markdown
# Model Card — <nombre del modelo, ej. "Late Fusion XGBoost + BioBERT-es v1">

## Detalles del modelo
- Versión: <tag/commit/fecha>
- Tipo: <early fusion / late fusion / baseline unimodal>
- Framework: <scikit-learn / XGBoost / TensorFlow-Keras / transformers>
- Fecha de entrenamiento:
- Responsable: <integrante del equipo>

## Uso previsto
- Caso de uso: apoyo a la decisión de triaje en urgencias, Resolución 5596/2015 (Colombia).
- Usuarios previstos: profesional de Medicina o Enfermería en el punto de triaje.
- **Uso NO previsto (explícito):** decisión autónoma sin validación humana; uso en poblaciones no
  representadas en los datos de entrenamiento (ej. pediatría, si no se incluyó explícitamente);
  uso fuera del contexto de urgencias hospitalarias colombiano sin re-validación.

## Datos de entrenamiento
- Fuentes: MIMIC-IV-ED v2.2 (preentrenamiento) + Hospital San Juan de Dios (fine-tuning).
- Tamaño: <n de MIMIC> + <n de San Juan de Dios> — completar con el n real, no aproximar.
- Periodo cubierto:
- Distribución de clases (I-V) en el conjunto de entrenamiento:

## Métricas de evaluación
- Conjunto de test: <tamaño, fuente, fecha de corte>
- Métricas globales (macro): F1, Precisión, Recall, AUC-ROC — con intervalo de confianza
  (ver `pruebas-estadisticas-comparacion-modelos.md`).
- Métricas por clase (I-V), con foco en I-II.
- Comparación estadística contra el segundo mejor modelo (McNemar/DeLong, valor p).

## Auditoría de equidad
- Resultado resumido de `auditoria-equidad-subgrupos.md` — brecha más relevante encontrada y su
  interpretación clínica.

## Calibración
- Brier score, resumen de la curva de calibración.
- Si no está calibrado: indicarlo explícitamente y no presentar la probabilidad de salida como
  una probabilidad clínica confiable hasta aplicar calibración post-hoc.

## Explicabilidad
- Técnica: SHAP (TreeExplainer / KernelExplainer según el modelo).
- Variables con mayor peso promedio (Top-5 a Top-10), en lenguaje clínico.

## Limitaciones conocidas
- <Completar con hallazgos reales de las fases 1-6 de `validacion-cientifica-ml`, nunca con
  limitaciones genéricas copiadas de la literatura>

## Consideraciones éticas
- Anonimización aplicada conforme a Ley 1581 de 2012.
- Autorización del Comité de Ética del Hospital San Juan de Dios (referencia/fecha).
- El sistema es de apoyo, no de decisión autónoma — el criterio humano prevalece siempre.
```
