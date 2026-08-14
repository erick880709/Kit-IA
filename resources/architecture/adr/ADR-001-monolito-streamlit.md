# ADR-001: Monolito Streamlit sobre frontend/backend separados

- **Estado:** Aceptado
- **Fecha:** 2026-08-13
- **Decisión relacionada en el documento:** `Documento_Arquitectura_TriajeIA.md` §4 y §11

## Contexto

La demo del TFM es académica y mono-usuario, con plazo acotado y con decisión de stack ya cerrada por `refinador` (RT-007: Streamlit, IA 14/100). Evaluamos separar UI y backend (Candidatas B y C de §4.2) para ganar extensibilidad futura.

## Decisión

Monolito modular Streamlit con capas aisladas (`views → services → domain → infra`), donde `domain/` no depende de Streamlit ni de infraestructura.

## Alternativas consideradas

- **React + FastAPI + PostgreSQL (Candidata B, 3.45):** descartada por costo de entrega y por complejidad desproporcionada para una demo mono-usuario.
- **FastAPI + Streamlit como dos contenedores (Candidata C, 3.70):** descartada por agregar un salto de red que complica la latencia (< 3 s, RNF-002) sin beneficio medible.

## Consecuencias

- **Positivas:** entrega rápida, un solo proceso (sin CORS, sin serialización extra), despliegue local trivial.
- **Negativas:** acoplamiento UI/lógica a mediano plazo. Mitigación: la frontera `domain/` pura permite evolucionar a FastAPI+React sin reescribir lógica.
- **Trigger de reevaluación:** despliegue multi-usuario real (hospitalario) → reabrir este ADR.
