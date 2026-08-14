# ADR-002: Selección de base de datos — SQLite en la demo, PostgreSQL como evolución

- **Estado:** Aceptado
- **Fecha:** 2026-08-13
- **Decisión relacionada en el documento:** `Documento_Arquitectura_TriajeIA.md` §9 (Paso 0.8 de `archi`)

## Contexto

Los datos operacionales son transaccionales y de bajo volumen: eventos de triaje (con esquema dual IA/profesional, RD-003), usuarios, auditoría. El patrón de acceso es de escritura puntual por evento y lectura para auditoría/reportes, sin concurrencia real (demo mono-usuario local).

## Clasificación de datos (guia-bases-de-datos)

| Dato | Naturaleza | Patrón de acceso | Motor elegido |
|---|---|---|---|
| Eventos de triaje, pacientes, usuarios, auditoría | Transaccional | Escrituras puntuales + lecturas de reporte | SQLite (SQLAlchemy) |
| Modelos versionados (joblib) + métricas | Artefactos binarios + metadatos | Escritura al entrenar, lectura al arrancar | Sistema de archivos + MLflow |
| Datasets crudos | Archivos CSV | Batch offline | Sistema de archivos (DVC/naming) |

## Decisión

SQLite 3 vía SQLAlchemy ORM para el contenedor `triaje-db`. El ORM abstrae el motor, de modo que la migración posterior no toca el dominio.

## Alternativas consideradas

- **PostgreSQL:** robusto pero exige servicio local/Docker — fricción innecesaria para la demo académica.
- **DuckDB:** excelente para analítica offline, pero no aporta sobre SQLite para OLTP de un solo usuario.
- **JSON plano:** descartado por pérdida de integridad referencial y consultas de auditoría.

## Consecuencias

- **Positivas:** arranque instantáneo, cero configuración, costo $0, backup trivial (archivo único).
- **Negativas:** sin concurrencia multi-usuario real; límites de volumen.
- **Trigger de reevaluación:** despliegue hospitalario o multi-usuario → migrar a PostgreSQL (el esquema ORM se conserva).
