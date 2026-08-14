---
id: HU-E2-02
type: Historia de Usuario
epic: 002-flujo-clinico-triaje
priority: Alta
points: 3
---

# HU-E2-02: Buscar Paciente Existente

## Como
Personal Administrativo / Enfermera de Triaje / Médico

## Quiero
Buscar un paciente ya registrado por documento, nombre o número de historia clínica

## Para
Recuperar sus datos sin tener que volver a capturarlos y consultar su historial

## Criterios de Aceptación
- [ ] CA1: Barra de búsqueda unificada que acepta: número de documento, nombre (parcial o completo), número de historia clínica
- [ ] CA2: Resultados paginados si hay más de 10 coincidencias
- [ ] CA3: Cada resultado muestra: nombre, documento, edad, fecha del último triaje, nivel asignado en ese triaje
- [ ] CA4: Al seleccionar un paciente, se navega a la pantalla de Registro con los datos demográficos precargados
- [ ] CA5: La búsqueda por nombre soporta coincidencias parciales (mínimo 3 caracteres) y tolerancia a errores tipográficos menores

## Recurso de datos involucrado
- **Nombre:** Paciente (consulta, no modifica)
- **Capa(s):** backend + frontend

## Subtareas
- [ ] Diseñar barra de búsqueda y lista de resultados
- [ ] Implementar endpoint de búsqueda con múltiples criterios
- [ ] Implementar paginación de resultados
- [ ] Implementar precarga de datos al seleccionar paciente
