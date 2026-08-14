---
id: TT-E1-04
type: Tarea Técnica
epic: 001-fundacion-del-sistema
priority: Alta
points: 5
---

# TT-E1-04: Crear Estructura Modular del Proyecto y Puntos de Extensión

## Descripción
Implementar la arquitectura modular por capas (UI / lógica de negocio / acceso a datos / motor IA) con configuración externalizada, y documentar los puntos de extensión para futura integración con Historia Clínica Electrónica y sistemas hospitalarios. Cubre RNF-007 y RF-INT-001/002.

## Criterios de Done
- [ ] Separación clara en módulos Python: `app/ui/`, `app/services/`, `app/data/`, `app/ia/`, `app/config/`
- [ ] Archivo `config.yaml` o `.env` para parámetros externalizados: tiempos de sesión, rangos de signos vitales, catálogos, rutas de modelos
- [ ] Interfaz documentada para el módulo de integración HCE (clase abstracta o protocolo Python con métodos: `obtener_antecedentes(paciente_id)`, `obtener_episodios_previos(paciente_id)`)
- [ ] Implementación por defecto de la interfaz HCE que devuelve datos vacíos (modo sin integración)
- [ ] Documentación de arquitectura: diagrama de componentes en `docs/arquitectura-componentes.md`
- [ ] Estrategia de logging configurada (Python logging, niveles INFO/WARNING/ERROR)

## Dependencias
TT-E1-01, TT-E1-02

## Subtareas
- [ ] Crear estructura de paquetes Python
- [ ] Implementar carga de configuración externalizada
- [ ] Definir interfaz de integración HCE
- [ ] Configurar sistema de logging
- [ ] Redactar documento de arquitectura de componentes
