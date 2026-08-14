---
id: HU-E6-02
type: Historia de Usuario
epic: 006-dashboard-gestion-modelos-analitica
priority: Media
points: 5
---

# HU-E6-02: Gestión de Modelos (CRUD, Versionado, Activación, Rollback)

## Como
Administrador IA

## Quiero
Registrar nuevos modelos, versionarlos, activar un modelo para producción y desactivarlo (rollback) si su desempeño degrada

## Para
Gestionar el ciclo de vida de los modelos de IA de forma controlada y auditable

## Criterios de Aceptación
- [ ] CA1: Pantalla "Gestión de Modelos" accesible solo para rol Administrador IA
- [ ] CA2: Listado de todos los modelos registrados con: nombre, versión actual, algoritmo, arquitectura, fecha de registro, estado (Activo/Inactivo/En validación), métricas principales
- [ ] CA3: Botón "Registrar Nuevo Modelo" → formulario: nombre, algoritmo, arquitectura (early/late), hiperparámetros, dataset usado, métricas (F1, Precision, Recall, AUC-ROC)
- [ ] CA4: El registro crea la versión 1.0 del modelo
- [ ] CA5: Botón "Nueva Versión" → mismo formulario con campos precargados, genera v1.1, v1.2, etc.
- [ ] CA6: Historial de versiones accesible desde cada modelo: lista de versiones con métricas comparativas
- [ ] CA7: Botón "Activar" sobre un modelo en validación → lo promueve a producción (solo puede haber un modelo activo a la vez). Genera registro de auditoría.
- [ ] CA8: Botón "Desactivar" (rollback) sobre el modelo activo → lo pasa a inactivo. El sistema debe tener al menos otro modelo registrado para revertir. Exige motivo del rollback. Genera registro de auditoría.

## Recurso de datos involucrado
- **Nombre:** Modelo (ENT-009 extendido para gestión)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdModelo | UUID | Sí | Generado automáticamente |
| Nombre | Texto | Sí | Unique |
| Descripcion | Texto | No | |
| Algoritmo | Texto | Sí | XGBoost, Random Forest, etc. |
| Arquitectura | Catálogo | Sí | Early Fusion, Late Fusion, Unimodal |
| Hiperparametros | JSON | Sí | Diccionario de hiperparámetros |
| DatasetEntrenamiento | Texto | Sí | Descripción del dataset |
| F1Score | Decimal | Sí | |
| Precision | Decimal | Sí | |
| Recall | Decimal | Sí | |
| AUCROC | Decimal | Sí | |
| AUPRC | Decimal | No | |
| Estado | Catálogo | Sí | Activo, Inactivo, En validación |
| Version | Texto | Sí | v1.0, v1.1, etc. |
| FechaRegistro | DateTime | Sí | Automático |
| RegistradoPor | UUID | Sí | FK a Usuario |
| MotivoRollback | Texto | No | Solo si se desactivó |

### Relaciones con otros recursos
- `PrediccionIA` (1:N): cada predicción referencia la versión del modelo usado
- `Auditoria` (1:N): cada cambio de estado genera registro

## Subtareas
- [ ] Diseñar pantalla de Gestión de Modelos
- [ ] Implementar CRUD de modelos
- [ ] Implementar versionado
- [ ] Implementar activación/desactivación con reglas de negocio
- [ ] Implementar historial de versiones con métricas comparativas
