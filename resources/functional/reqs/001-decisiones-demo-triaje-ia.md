---
id: 001
slug: decisiones-demo-triaje-ia
ia_cierre: 14/100
rondas: 1
estado: lista-para-diseno
fecha: 2026-08-13
---

# Decisiones de Producto — Demo del Sistema de Triaje Multimodal IA

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 EVOLUCIÓN DEL ÍNDICE DE AMBIGÜEDAD
 Ronda 0 (inicial): 47/100
 Ronda 1:          14/100  ← CIERRE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## NECESIDAD DE NEGOCIO REFINADA

Definir de forma vinculante las decisiones de producto pendientes del sistema de triaje multimodal IA (demo TFM): stack Streamlit, alcance de datos del paciente con campos clínicos complementarios (grupo sanguíneo y alergias), datos sintéticos calibrados con los datasets reales, comparativa IA-profesional sin modo a ciegas, y alcance completo del dashboard y gestión de modelos para la defensa.

## Fuente(s) de origen

- `resources/architecture/definitions/RT-007-stack-demo-streamlit-flask.md`
- `resources/functional/hu/tt-e7-01-extender-schema-paciente.md`
- `resources/functional/reqs/desglose-epicas-tfm.md`
- `context/05-PENDIENTES-PARA-DIRECTORA.md`

## Justificación

Sin estas decisiones, `archi`, `genesis` y `builder` no pueden avanzar sin supuestos. Los campos clínicos adicionales (grupo sanguíneo, alergias) son necesarios para la seguridad de la medicación en la historia clínica del paciente.

## Actores

| Rol | Tipo | Responsabilidad |
|---|---|---|
| Equipo TFM | Ejecutor | Implementa la demo |
| Damaris Fuentes Lorenzo | Aprobadora | Valida decisiones formales |
| Tribunal UNIR | Beneficiario | Evalúa el resultado |
| Profesionales de salud | Beneficiarios | Validan la demo |

## Alcance

- ✅ IN SCOPE: Demo en **Streamlit** (decisión definitiva) · Python 3.12 · los 9 campos personales TT-E7 **+ TipoSangre + Alergias (con cuál alergia)** como campos clínicos complementarios · datos sintéticos ~100-200 pacientes generados **con las distribuciones reales de los datasets en `datasets/`** · email de recuperación simulado con token · E6 (Dashboard + Gestión de Modelos) como **Must Have** · late fusion con promedio ponderado por defecto · TLS self-signed documentado.
- ❌ OUT OF SCOPE: Modo "a ciegas" de la comparativa IA-profesional (se documenta el sesgo de anclaje en el TFM) · SMTP real · integración HCE real · alta disponibilidad.

## Criterios de Aceptación

```
DADO un paciente registrado en la demo
CUANDO se ingresa a urgencias
ENTONCES el formulario captura los 11 campos personales/clínicos
(9 de TT-E7 + tipo de sangre + alergias) con validación

DADO el arranque de la demo
CUANDO se ejecuta el comando de inicio
ENTONCES Streamlit levanta la app con datos sintéticos calibrados
con las distribuciones reales de datasets/

DADO una recuperación de contraseña
CUANDO el usuario la solicita
ENTONCES se emite un token simulado de un solo uso con expiración

DADO el dashboard
CUANDO un evaluador lo consulta
ENTONCES muestra los indicadores operativos y de concordancia
como funcionalidad Must Have de la defensa
```

## Restricciones y Supuestos

- **Restricciones:** Streamlit (decidido) · datos demo sintéticos, nunca datos reales en vivo · anonimización Ley 1581 en toda exportación.
- **Supuestos validados:** email simulado · TLS self-signed local · promedio ponderado en late fusion.
- **Supuestos no validados:** ninguno bloqueante.

## Métricas de Éxito

| Métrica | Línea Base | Meta | Plazo |
|---|---|---|---|
| Modelo (F1/Prec/Recall/AUC) | — | ≥ 0,82 / 0,85 / 0,80 / 0,87 | Defensa TFM |
| Inferencia | — | < 3 s | Demo funcional |
| Distribución datos demo vs reales | — | Desviación por nivel ≤ ±2 pp | Demo funcional |
| Concordancia IA-profesional | — | % global y por nivel reportado | Dashboard |

## Prioridad (MoSCoW)

- **Must Have:** E1-E6 completas (incluye Dashboard y Gestión de Modelos) · campos clínicos del paciente · comparativa con registro dual.
- **Should Have:** exportaciones PDF/Excel/CSV.
- **Could Have:** Docker para la demo · grabación en video de respaldo.
- **Won't Have (este alcance):** modo a ciegas · SMTP real · integración HCE.

## Dependencias

- Datasets reales ya descargados en `datasets/` (triage, BDUA ×2, morbilidad, cohorte hospital) para calibrar los sintéticos.
- Modelo serializado (TT-E3-09) para la demo.
- Decisión formal de Streamlit → actualizar `RT-007` y supuestos del desglose.

## Brechas pendientes

Ninguna — **✅ Lista para diseño/estimación.**
