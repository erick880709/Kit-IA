# ADR-005 — Verificación de integridad previa a la deserialización de artefactos ML

- **Estado:** Aceptado · **Fecha:** 2026-08-14
- **Contexto:** hallazgo MUR-01 de la auditoría de seguridad (bloqueante).

## Decisión

`cargar_paquete()` verifica el hash SHA-256 del manifiesto **antes** de
invocar `joblib.load`; la comparación usa `secrets.compare_digest` y la carga
falla cerrada (`fail-closed`) si el manifiesto no existe o no trae hash. El
manifiesto se escribe siempre en el mismo directorio del artefacto.

## Alternativas consideradas

1. Verificar después de cargar (estado anterior): desechada — `joblib.load`
   deserializa pickle, que ejecuta código arbitrario; la verificación
   posterior no protege nada.
2. No persistir artefactos y reentrenar en cada arranque: desechada — rompe
   el presupuesto RNF-007 y la experiencia demo.
3. Firma criptográfica asimétrica: sobredimensionada para la demo; queda como
   evolución de producción.

## Consecuencias

- El servicio de inferencia conserva su fallback manual ante un artefacto
  rechazado (el flujo clínico nunca se bloquea).
- Cualquier reempaquetado manual de artefactos sin regenerar manifiesto es
  rechazado — documentado en `ml/src/registry.py`.

## Evidencia

Tests que fallan sobre el código anterior:
`test_cargar_paquete_verifica_hash_antes_de_deserializar`,
`test_cargar_paquete_rechaza_artefacto_sin_manifiesto`,
`test_serializar_paquete_escribe_manifiesto_junto_al_artefacto`.
