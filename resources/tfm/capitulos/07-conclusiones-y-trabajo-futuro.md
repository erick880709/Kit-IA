# 7. Conclusiones y trabajo futuro — TriajeIA

## 7.1 Conclusiones

1. **El sistema se construyó y quedó operativo.** TriajeIA implementó de
   extremo a extremo el flujo clínico de triaje (registro → signos →
   evaluación → clasificación IA explicable → cierre con informe), con RBAC,
   auditoría inmutable, dashboard y gestión de modelos, respaldado por 103
   pruebas automatizadas en verde, análisis estático sin errores y un pipeline
   de integración continua que reproduce los mismos gates.

2. **El diseño multimodal con fusión tardía demostró ser estadísticamente
   superior a la línea base mayoritaria.** Sobre el test del dataset sintético
   el modelo alcanzó exactitud 0.978 y AUC-ROC 0.968, con McNemar p ≈ 0 frente
   a la regla de clase mayoritaria, y calibración adecuada (Brier 0.036,
   ECE 0.042). Los niveles clínicamente prioritarios lograron un desempeño
   razonable (nivel II: recall 0.812, precisión 0.867) gracias a los umbrales
   por clase que priorizan la sensibilidad en I–II.

3. **Las metas cuantitativas completas (RNF-001) no se alcanzaron y se declara
   con honestidad.** Macro-F1 0.551 frente a la meta de 0.82; precisión 0.560
   frente a 0.85; recall 0.542 frente a 0.80. La causa identificada no es el
   diseño de fusión sino la naturaleza de los datos disponibles: clases I y V
   con soportes de 2–3 registros en test, y un componente textual real (SJdD)
   débil por sí solo (macro-F1 0.088 en holdout). El AUC propio no es
   comparable con los benchmarks de la literatura porque el CIE-10 sintético
   está condicionado al nivel de triaje.

4. **El rigor experimental quedó verificado como parte del propio trabajo.**
   Se corrigieron dos fuentes de fuga de datos detectadas en auditoría
   (escalador ajustado con todo el dataset; holdout evaluado con el modelo que
   lo entrenó) y un hallazgo de seguridad bloqueante (deserialización de
   artefactos sin verificación previa de integridad), dejando evidencia
   reproducible de cada corrección.

## 7.2 Limitaciones específicas encontradas

- **Dataset de evaluación limitado y parcialmente sintético:** la evidencia
  cuantitativa principal proviene de un demo sintético; no sustituye una
  validación prospectiva.
- **Clases críticas insuficientes:** los niveles I y V no se aprenden con los
  volúmenes disponibles (distribución real: I 0.23 %, V 0.46 %).
- **Componente textual real débil:** el TF-IDF sobre CIE-10+texto no captura
  semántica clínica (alternativas: embeddings clínicos/BERT); su aporte en la
  cohorte SJdD es marginal.
- **Validación externa pendiente:** MIMIC-IV-ED requiere credenciales
  PhysioNet; sin ella no es posible afirmar generalización.
- **Ámbito de despliegue:** demo local monousuario; quedan pendientes los
  refuerzos de producción identificados en la auditoría OWASP (secret key
  obligatoria, login sin enumeración de cuentas, rate-limit en recuperación,
  TLS y headers de seguridad).

## 7.3 Trabajo futuro

- Obtener la **autorización del Comité de Ética** (requisito bloqueante,
  Art. 2.7 UNIR) y validar el sistema con datos clínicos reales anonimizados.
- Validación externa con **MIMIC-IV-ED** y, de ser posible, un piloto
  prospectivo en un servicio de urgencias colombiano.
- Sustituir el submodelo textual por representaciones semánticas
  (embeddings clínicos en español) y re-evaluar la fusión.
- Recoger datos suficientes de niveles I y II (o aplicar aprendizaje con pocos
  ejemplos / síntesis controlada) para elevar el recall crítico hacia la meta
  de 0.80.
- Cerrar los hallazgos de producción de la auditoría de seguridad y desplegar
  con monitoreo continuo de métricas del modelo (drift, calibración).
