"""Capa de dominio: entidades y reglas de negocio puras.

Sin dependencias de Streamlit ni de infraestructura (frontera que permite
evolucionar a FastAPI/React sin reescribir lógica — ADR-001 del documento
de arquitectura). Las entidades las agrega `builder` a partir de
`resources/design/data-model.md`.
"""
