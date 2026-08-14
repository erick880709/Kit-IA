---
id: TT-E1-02
type: Tarea Técnica
epic: 001-fundacion-del-sistema
priority: Alta
points: 8
---

# TT-E1-02: Configurar Base de Datos y Modelo de Dominio

## Descripción
Implementar el esquema de base de datos SQLite con las 12 entidades del dominio (ENT-001 a 012), sus relaciones, restricciones de integridad y principios de integridad definidos en RD-002.

## Criterios de Done
- [ ] Esquema SQLite creado con tablas para: Paciente, EventoTriaje, SignosVitales, MotivoConsulta, AntecedentesClinicos, EscalaDolor, EvaluacionClinica, TextoClinico, PrediccionIA, ExplicacionSHAP, ProfesionalSalud, Auditoria
- [ ] ENT-002 EventoTriaje incluye los campos extendidos: NivelSugeridoIA, ProbabilidadesIA (JSON), NivelAsignadoProfesional, Concordancia (calculado), MotivoDiscrepancia, VersionModeloUsado
- [ ] ENT-001 Paciente incluye campos nuevos: ViaLlegada (catálogo), EpisodiosPreviosUrgencias
- [ ] Claves foráneas y restricciones de integridad implementadas según cardinalidades del RD-002
- [ ] Script de migración/creación de tablas ejecutable (`python init_db.py`)
- [ ] Datos semilla para catálogos: niveles triaje (I-V), roles, estados, vías de llegada, niveles de conciencia
- [ ] Mapeo ORM o capa de acceso a datos implementada (SQLAlchemy o sqlite3 directo)

## Dependencias
TT-E1-01 (estructura del proyecto creada)

## Subtareas
- [ ] Diseñar esquema SQL completo en un archivo `schema.sql`
- [ ] Implementar script `init_db.py`
- [ ] Insertar datos semilla de catálogos
- [ ] Implementar capa de acceso a datos (DAO/Repository)
- [ ] Escribir test de integridad referencial
