---
id: TT-E4-01
type: Tarea Técnica
epic: 004-motor-ia-explicabilidad-demo
priority: Alta
points: 3
---

# TT-E4-01: Servicio de Carga del Modelo Serializado

## Descripción
Implementar el módulo que carga el modelo ganador + transformadores (scaler, encoder, tokenizador) al iniciar la aplicación, y lo mantiene en memoria para inferencias sucesivas sin recargar.

## Criterios de Done
- [ ] Módulo `model_loader.py` que usa el script `load_model.py` de TT-E3-09
- [ ] Carga del modelo al iniciar la app (no en cada inferencia)
- [ ] Warm-up: ejecutar una inferencia de prueba al cargar para verificar que el modelo funciona
- [ ] Si el modelo no se puede cargar, la app inicia en modo degradado (sin IA) y lo registra en log
- [ ] La versión del modelo cargado se muestra en la UI (ej. sidebar: "Modelo activo: XGBoost Early Fusion v1.2")

## Dependencias
TT-E3-09 (modelo serializado disponible)

## Subtareas
- [ ] Implementar model_loader.py
- [ ] Implementar carga lazy al iniciar la app
- [ ] Implementar warm-up de inferencia
- [ ] Implementar modo degradado si falla la carga
