---
id: HU-09
type: Historia de Usuario
epic: MIGRACION-REACT
priority: Media
points: 3
---

# HU-09: Gestión de modelos IA

## Como
Administrador del sistema

## Quiero
Ver los modelos de IA registrados, activar un modelo diferente, registrar nuevos modelos desde disco, y consultar el estado del servicio de inferencia

## Para
Gestionar el ciclo de vida de los modelos de Machine Learning sin necesidad de reinicios ni comandos manuales

## Criterios de Aceptación

- [ ] CA1: La página muestra el estado del servicio de inferencia: ✅ Activo (con versión y features) o ❌ No cargado.
- [ ] CA2: **Panel de umbrales y detalles**: expander que muestra:
  - Tabla de umbrales por clase (Nivel I-V con su valor de threshold).
  - Información del modelo en formato JSON legible (nombre, versión, n_features, shap_disponible, directorio).
- [ ] CA3: **Tabs**:
  - "💾 Modelos Serializados": lista de modelos encontrados en disco con: nombre, versión, estado (🟢 ACTIVO / ⚪ Inactivo), F1 Macro, tamaño, fecha. Cada modelo inactivo tiene botón "🟢 Activar".
  - "🗄️ Registro BD": modelos registrados en la base de datos.
  - "➕ Registrar Modelo": formulario para registrar un nuevo modelo desde una ruta en disco.
- [ ] CA4: Al activar un modelo, se llama a `PATCH /api/models/{id}` y el cambio se refleja inmediatamente (sin recargar).
- [ ] CA5: Botón "🔄 Recargar Modelo" para recargar el modelo activo desde disco (`POST /api/inference/reload`).
- [ ] CA6: **Estado del Servicio** (expander al final): muestra información técnica del `InferenceService`: modelo cargado, device, embedding_dim, scaler, encoder.

## Recurso de datos involucrado

- **Nombre del recurso:** Modelo
- **Capa(s):** frontend (consume GET/POST/PATCH /api/models, GET /api/inference/status, POST /api/inference/reload)

## Subtareas

- [ ] Crear `pages/ModelManagementPage.tsx`
- [ ] Implementar panel de estado del servicio
- [ ] Implementar panel de umbrales y detalles
- [ ] Implementar tabs: serializados, BD, registrar
- [ ] Implementar activación/recarga de modelo
- [ ] Probar cambio de modelo activo
