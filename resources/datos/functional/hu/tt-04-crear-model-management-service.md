---
id: TT-04
type: Tarea Técnica
epic: MIGRACION-REACT
priority: Alta
points: 3
dependencies: "Ninguna"
---

# TT-04: Crear ModelManagementService

## Descripción

Actualmente `model_management_page.py` ejecuta consultas SQL directas para gestionar el registro de modelos IA en la base de datos. También escanea el disco para encontrar modelos serializados. Hay que extraer esta lógica a un nuevo servicio `ModelManagementService`.

Operaciones a implementar:
- `list_models() -> List[Dict]`: listar modelos registrados en la tabla `Modelo`.
- `register_model(name, version, path, metadata) -> Dict`: insertar un nuevo modelo en la BD.
- `activate_model(id) -> Dict`: marcar un modelo como activo (y desactivar los demás).
- `scan_disk_models(models_dir) -> List[Dict]`: escanear el directorio `models/` y detectar modelos serializados (carpetas con `model.joblib` + `metadata.json`).
- `get_active_model() -> Optional[Dict]`: obtener el modelo activo actual.

## Criterios de Done

- [ ] Archivo `app/services/model_management_service.py` creado con clase `ModelManagementService`.
- [ ] Constructor recibe `db_path: str`.
- [ ] Métodos `list_models()`, `register_model()`, `activate_model()`, `scan_disk_models()`, `get_active_model()` implementados.
- [ ] `activate_model()` es atómico: desactiva el modelo previo y activa el nuevo en una transacción.
- [ ] `scan_disk_models()` detecta modelos por presencia de `model.joblib` + `metadata.json` en subdirectorios.
- [ ] `model_management_page.py` se actualiza para usar el servicio en vez de SQL directo.
- [ ] La página de gestión de modelos de Streamlit sigue funcionando.
- [ ] Sin dependencias de Streamlit en el nuevo servicio.

## Recurso de datos involucrado

- **Nombre del recurso:** Modelo
- **Capa(s):** backend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| id | int | Sí (auto) | PK |
| nombre | str | Sí | Ej: "Early Fusion" |
| version | str | Sí | Ej: "v20260720_224350" |
| ruta | str | Sí | Ruta absoluta al directorio del modelo |
| activo | bool | Sí | Solo un modelo puede estar activo a la vez |
| fecha_registro | datetime | Sí (auto) | Timestamp de registro |
| metadata | dict | No | Copia del metadata.json del modelo |
| f1_macro | float | No | Métrica F1 del modelo |
| auc_roc | float | No | Métrica AUC-ROC del modelo |

### Relaciones con otros recursos
- `Triaje` (1:N): un modelo puede haber generado múltiples predicciones de triaje.

## Subtareas

- [ ] Identificar queries SQL exactas en `model_management_page.py`
- [ ] Crear `ModelManagementService` con los 5 métodos
- [ ] Implementar `scan_disk_models()` usando `pathlib`
- [ ] Actualizar `model_management_page.py` para usar el servicio
- [ ] Verificar que la gestión de modelos sigue funcionando en Streamlit
