---
id: 004
slug: motor-ia-explicabilidad-demo
tipo: epica
prioridad: Must-Have
orden: 3
dependencias: E1, E2, E3
fecha: 2026-07-19
---

# ÉPICA 4 — Motor de IA en la Demo y Explicabilidad

## Necesidad de Negocio

Integrar el modelo entrenado (producto de la Épica 3) en la aplicación demo (producto de la Épica 2), cerrando el circuito completo: el profesional captura datos clínicos → el sistema ejecuta inferencia multimodal → muestra el nivel sugerido con probabilidades, confianza y explicación SHAP en lenguaje clínico → el profesional valida con su propio criterio. Esta épica es donde el sistema demuestra su valor: la IA apoyando (no reemplazando) al clínico.

## Justificación

El objetivo central del TFM es validar que un sistema multimodal con explicabilidad puede asistir el triaje en Colombia. La Épica 2 construyó el formulario, la Épica 3 entrenó el modelo — esta épica los une y entrega la experiencia completa que se sustentará ante el tribunal.

## Actores

| Rol | Tipo | Responsabilidad |
|-----|------|-----------------|
| Enfermera de Triaje / Médico | Ejecutor | Disparar la inferencia, revisar SHAP, registrar su clasificación |
| Científico de Datos | Soporte | Garantizar que el modelo carga correctamente y la inferencia es reproducible |
| Investigador | Beneficiario | Usar la pantalla de comparación de modelos para el Cap. 5 |

## Alcance

- ✅ IN SCOPE:
  - Carga del modelo serializado + scaler + encoder + tokenizador al iniciar la app
  - Ejecución de inferencia asíncrona (no bloquea la UI, muestra spinner)
  - Visualización de probabilidades por nivel (I-V) en gráfico de barras
  - Selección de predicción con umbral optimizado por clase (no argmax puro)
  - Registro de: nivel sugerido, probabilidades (JSON), confianza, versión del modelo, tiempo de inferencia
  - Generación y visualización de explicación SHAP (TreeExplainer para RF/XGBoost)
  - Top 5-10 variables en lenguaje clínico comprensible
  - Gráficos: barras horizontales SHAP, waterfall plot, force plot
  - Comparación implícita con criterios MTS/Manchester cuando coincidan
  - Campo independiente `NivelAsignadoProfesional` (nunca se autocompleta con la IA)
  - Cálculo automático de concordancia IA vs. profesional
  - Exigencia de `MotivoDiscrepancia` cuando Concordancia = No
  - Pantalla de comparación de modelos (early vs. late fusion lado a lado)
  - Modo degradado: si el modelo no está disponible, se permite clasificación manual
  - Tiempo de inferencia objetivo < 3 segundos

- ❌ OUT OF SCOPE:
  - Reentrenamiento del modelo desde la demo
  - Cambio de modelo activo en caliente (requiere reinicio de la app en la demo)
  - Explicabilidad en tiempo real para modelos de deep learning (KernelExplainer)

## Criterios de Aceptación

```
DADO que el profesional completó la evaluación clínica y presiona "Ejecutar IA"
CUANDO el modelo está disponible y los datos son válidos
ENTONCES en menos de 3 segundos se muestra el nivel sugerido, probabilidades por nivel y la explicación SHAP

DADO que el texto libre del motivo de consulta está vacío
CUANDO se ejecuta la inferencia
ENTONCES el pipeline continúa usando solo variables estructuradas sin error

DADO que la IA sugiere Nivel II con probabilidad 0.72
CUANDO el profesional revisa la explicación SHAP
ENTONCES ve que "SpO₂ 88%" aparece como la variable de mayor peso, en lenguaje clínico comprensible

DADO que el profesional asigna Nivel III cuando la IA sugirió Nivel II
CUANDO intenta cerrar el evento sin registrar el motivo de discrepancia
ENTONCES el sistema impide el cierre y exige el campo MotivoDiscrepancia

DADO que el servicio de inferencia no responde (timeout)
CUANDO el profesional presiona "Ejecutar IA"
ENTONCES el sistema muestra "Modelo no disponible" y permite continuar con clasificación manual

DADO que el investigador accede a la pantalla de Comparación de Modelos
CUANDO selecciona early fusion y late fusion para comparar
ENTONCES ve métricas lado a lado (F1, Precision, Recall, AUC-ROC, matriz de confusión) sobre el mismo caso
```

## Métricas de Éxito

| Métrica | Línea Base | Meta | Plazo |
|---------|-----------|------|-------|
| Tiempo de inferencia (end-to-end) | No existe | < 3 segundos (RNP-001) | Cierre de E4 |
| Cobertura del contrato de salida XAI | 0 | 4/4 elementos (nivel+prob+versión, SHAP top, comparación MTS, tiempo) | Cierre de E4 |
| Modo degradado funcional | No existe | Clasificación manual disponible cuando IA no responde | Cierre de E4 |
| Concordancia IA vs. profesional registrada | No existe | 100% de eventos cerrados tienen ambos campos (NivelSugeridoIA y NivelAsignadoProfesional) | Cierre de E4 |
| Reproducibilidad de inferencia | No existe | Misma entrada → misma predicción en cualquier ejecución de la demo | Cierre de E4 |

## Prioridad (MoSCoW)

- **Must Have:** Inferencia asíncrona, visualización de probabilidades, SHAP con top variables en lenguaje clínico, campo independiente del profesional, concordancia, modo degradado, <3s
- **Should Have:** Waterfall plot, force plot, comparación con MTS/Manchester
- **Could Have:** SHAP en segundo plano (mostrar predicción inmediatamente y SHAP cuando esté listo), comparación de modelos en tiempo real
- **Won't Have (en este alcance):** Explicabilidad contrafactual (qué tendría que cambiar para que el nivel fuera otro), SHAP para deep learning en producción

## Dependencias

- **E1 (Fundación):** Login, roles, estructura del proyecto
- **E2 (Flujo Clínico):** Pantallas de Evaluación Clínica y Clasificación IA construidas
- **E3 (Pipeline):** Modelo serializado + transformadores disponibles

## Archivos Janus que cubre

| Archivo | Tipo |
|---|---|
| `RF-IA-modulo-inteligencia-artificial.md` | Funcional |
| `RF-XAI-modulo-explicabilidad.md` | Funcional |
| `RT-006-explicabilidad-shap-xai.md` | Técnico |
| `RNF-001-rendimiento-inferencia-concurrencia.md` | No funcional |
| `RNF-002-disponibilidad-escalabilidad.md` | No funcional |
