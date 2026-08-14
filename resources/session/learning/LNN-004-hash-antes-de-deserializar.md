---
fecha: 2026-08-14
fase: entrega
tags: [seguridad, ml, pickle, deserializacion]
severidad: alta
---

# LNN-004: Verificar el hash ANTES de deserializar pickle/joblib (CWE-502)

## Contexto

En `ml/src/registry.py`, `cargar_paquete()` ejecutaba `joblib.load(ruta)` y **después** comparaba el sha256 del manifiesto. `joblib.load` deserializa pickle, y pickle ejecuta código arbitrario: un artefacto manipulado se ejecuta aunque el hash no coincida — la verificación posterior no protege nada.

## Regla

1. Calcular y verificar el hash del artefacto **antes** de llamar a `joblib.load`/`pickle.load`.
2. Comparar con `secrets.compare_digest` (timing-safe).
3. Fail-closed: sin manifiesto o sin hash → rechazar la carga (el fallback del servicio absorbe el error sin romper el flujo).
4. Escribir el manifiesto SIEMPRE junto al artefacto (mismo directorio), no en una carpeta fija distinta.

## Evidencia

Tres tests TDD que fallan sobre el código vulnerable: `test_cargar_paquete_verifica_hash_antes_de_deserializar`, `test_cargar_paquete_rechaza_artefacto_sin_manifiesto`, `test_serializar_paquete_escribe_manifiesto_junto_al_artefacto` (Muralla MUR-01, hardening-triaje-ia.md).
