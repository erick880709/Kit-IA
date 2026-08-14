---
id: HU-E6-02
type: Historia de Usuario
epic: E6 - Gestión de Modelos, Dashboard y Analítica
priority: High
points: 5
---

# HU-E6-02: Gestión de modelos (registro, versionado, activación, rollback)

## Como
Administrador / Investigador

## Quiero
registrar, versionar, activar y desactivar modelos

## Para
controlar qué versión del modelo está en producción en la demo (RF-008, RF-MOD-001 a 005).

## Criterios de Aceptación
- [ ] CA1: Registro de modelo con versión, algoritmo, fecha, id y métricas resumidas.
- [ ] CA2: Activación de una versión como activa; rollback a versión anterior con un clic.
- [ ] CA3: Historial completo de activaciones/desactivaciones.
- [ ] CA4: Solo roles autorizados cambian el modelo activo (RF-IA-008).

## Dependencias
TT-E3-09 + E4 completo
