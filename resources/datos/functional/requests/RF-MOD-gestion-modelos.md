# RF-MOD: Módulo de Gestión de Modelos

**Tipo:** Requerimiento funcional
**Fuente:** CONTEXT TRIA.txt — Sección 49, Módulo Gestión de Modelos; 02-ESPECIFICACION-TECNICA-MODELOS-IA.md
**Prioridad:** Alta

## Descripción
El sistema permitirá registrar, versionar, activar, desactivar (rollback) y comparar modelos de IA. Este módulo es esencial para la gobernanza del ciclo de vida de los modelos, habilitando la coexistencia de múltiples versiones (ej. early fusion y late fusion en paralelo durante la fase de validación) y la trazabilidad de qué modelo generó cada predicción.

## Actores involucrados
- Administrador IA (principal)
- Científico de Datos
- Investigador

## Criterios de aceptación

### RF-MOD-001 — Registrar Nuevo Modelo
- Formulario de registro con: nombre del modelo, algoritmo, arquitectura (early/late fusion), hiperparámetros, dataset de entrenamiento, métricas de desempeño (F1, Precision, Recall, AUC-ROC, AUPRC).
- El registro genera una versión inicial (v1.0).
- Solo usuarios con rol Administrador IA pueden registrar modelos.

### RF-MOD-002 — Versionado de Modelos
- Cada reentrenamiento o ajuste de hiperparámetros genera una nueva versión del modelo.
- El historial completo de versiones se mantiene accesible.
- Cada versión conserva: fecha de creación, métricas, dataset utilizado, hiperparámetros, estado (activo/inactivo/en validación).

### RF-MOD-003 — Activar Modelo (Promoción a Producción)
- Un modelo en estado "en validación" puede ser promovido a "activo" (producción) por el Administrador IA.
- La promoción requiere que el modelo tenga métricas registradas que cumplan los criterios mínimos (RNA-008).
- Solo puede haber un modelo activo a la vez para inferencia en producción.
- La activación genera un registro de auditoría.

### RF-MOD-004 — Desactivar Modelo (Rollback)
- Permite desactivar el modelo actualmente en producción y revertir a una versión anterior.
- La desactivación no elimina el modelo ni sus predicciones históricas.
- Genera registro de auditoría con el motivo del rollback.

### RF-MOD-005 — Historial Completo de Versiones
- Acceso al historial de todas las versiones de todos los modelos registrados.
- Visualización de métricas comparativas entre versiones.
- Trazabilidad: cada predicción almacena la versión del modelo que la generó (RNA-005), y desde este historial se puede recuperar el modelo exacto para reproducibilidad (RNA-004).

## Dependencias / relacionados
- RNA-004: Toda inferencia debe ser reproducible.
- RNA-005: La versión del modelo se almacena con cada predicción.
- RNA-006: El sistema permite coexistencia de múltiples versiones para comparación y validación.
- RNA-007: No se usarán modelos no validados clínicamente en producción.
- RNA-008: El modelo debe registrar métricas antes de ser promovido.
- RF-IA-007: Comparación de Modelos.
- `02-ESPECIFICACION-TECNICA-MODELOS-IA.md`: early fusion y late fusion coexisten como versiones distintas del modelo.

## Notas del analista
- La coexistencia de early y late fusion se implementa como dos modelos registrados independientemente (o dos versiones del mismo modelo con arquitecturas diferentes), habilitando la comparación requerida por RF-IA-007.
- El rollback (RF-MOD-004) es crítico para un entorno clínico real: si una nueva versión degrada el desempeño, debe poder revertirse inmediatamente.
