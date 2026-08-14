# Línea Base — TriajeIA (TFM UNIR)

> Generada por `archi` (Paso 0.5) el 2026-08-13 a partir de `resources/architecture/definitions/` (RNF/RT de janus), `resources/design/models/` (RD) y decisiones cerradas de `refinador` (IA 14/100). Una futura corrida de `archi` sobre este proyecto debe leer este archivo antes de volver a preguntar.

## Bloques resueltos (con trazabilidad)

| Bloque | Decisión | Fuente |
|---|---|---|
| Contexto de negocio | Triaje 5 niveles Res. 5596/2015, tiempos reales validados (I 28 min, II 22, III 35, IV 74, V 79) | RD-001 |
| Stack | Python 3.12 + **Streamlit** (demo funcional) | RT-001, RT-007, refinador |
| Fuentes de datos | MIMIC-IV-ED, cohorte SJdD (43.594), datos.gov.co (89.453 triajes), BDUA, Línea 123 | RT-006, RNF-004 |
| Métricas de modelo | F1 ≥ 0.82 · P ≥ 0.85 · R ≥ 0.80 · AUC ≥ 0.87 · recall I–II prioritario | RNF-001, RNF-003 |
| Modelo | Baselines obligatorios + BERT clínico español + fusión temprana Y tardía | RT-002/003/004/010 |
| Explicabilidad | SHAP con traducción a lenguaje clínico | HU-E4-02 |
| Umbrales | Tuning por clase optimizando recall I–II | RT-009, RNF-003 |
| Privacidad | Ley 1581/2012, anonimización, demo con datos sintéticos, Art. 2.7 UNIR | RNF-006, refinador |
| Datos demo | Sintéticos calibrados con distribuciones reales; 11 campos de paciente | Refinador, RD-002 |
| Autenticación | Local (bcrypt) + token simulado por email; bloqueo 3 intentos | HU-E1-04, refinador |
| Alcance E6 | Dashboard + Gestión de modelos = Must Have | Refinador |
| Modo "a ciegas" | Fuera de alcance | Refinador |
| Modelo de datos | Catálogo ENT-001..012 + registro dual IA/profesional (RD-003) | RD-002, RD-003 |
| Pantallas | 8 flujo principal + 4 soporte (fase 2) | RD-004, RD-005 |
| Despliegue | Local (demo académica); Community Cloud opcional; sin comparativo multi-nube | Sección 12 doc. arquitectura |

## Bloques abiertos (no bloqueantes)

- Nombres/campos exactos de ENT-006, ENT-007, ENT-010–ENT-012 (supuesto #1 del documento de arquitectura).
- Acceso efectivo a MIMIC-IV-ED (CITI pendiente).
- Decisión de publicar la demo en Community Cloud (pendiente de usuario).

## Arquitectura propuesta

Monolito modular Streamlit (Candidata A) — detalle, ADRs y candidatas descartadas en `resources/architecture/Documento_Arquitectura_TriajeIA.md`.
