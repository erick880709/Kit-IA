---
id: TT-E3-01
type: Tarea Técnica
epic: 003-pipeline-datos-entrenamiento-modelo
priority: Alta
points: 8
---

# TT-E3-01: Pipeline de Ingesta y Anonimización de Datos

## Descripción
Implementar el módulo de ingesta que lee datos de las 5 fuentes (MIMIC-IV-ED, Hospital San Juan de Dios, BDUA, datos.gov.co, Supersalud), las unifica en un formato común y ejecuta la anonimización obligatoria según Ley 1581 de 2012 (eliminación de identificadores directos, transformación de indirectos).

## Criterios de Done
- [ ] Script `ingest.py` que lee cada fuente en su formato nativo (CSV para la mayoría, formato MIMIC para PhysioNet)
- [ ] Unificación de esquemas: todas las fuentes mapeadas a las entidades del dominio (ENT-001 a 008)
- [ ] Paso de anonimización explícito y auditable: elimina Nombre, NumeroDocumento, Direccion, Telefono, Email
- [ ] Transformación de identificadores indirectos: FechaNacimiento → Edad (años), Municipio → Departamento
- [ ] Log detallado de: registros ingresados por fuente, registros descartados por anonimización, registros unificados
- [ ] Validación post-anonimización: verificar que no queden identificadores directos en el dataset de salida

## Dependencias
TT-E1-01 (entorno Python), TT-E1-02 (esquema de entidades)

## Subtareas
- [ ] Implementar lector de MIMIC-IV-ED (formato CSV de PhysioNet)
- [ ] Implementar lector de CSVs colombianos (datos.gov.co, BDUA, Supersalud)
- [ ] Implementar lector de registro Hospital San Juan de Dios
- [ ] Implementar unificación de esquemas
- [ ] Implementar anonimización
- [ ] Implementar logs de auditoría de ingesta
