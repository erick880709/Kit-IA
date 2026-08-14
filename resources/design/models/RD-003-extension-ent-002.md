# RD-003: Extensión ENT-002 — Registro Dual IA vs. Profesional

**Tipo:** Información de diseño
**Fuente:** `context/06-CAPTURA-SINTOMAS-Y-COMPARATIVA-IA-PROFESIONAL.md` §4

## Descripción
El campo genérico `NivelAsignado` de ENT-002 es insuficiente para la comparativa IA vs. profesional. Se reemplaza por un esquema dual:

| Campo | Tipo | Obligatorio | Quién lo llena |
|---|---|---|---|
| NivelSugeridoIA | Catálogo I–V | Sí (si se ejecutó inferencia) | Sistema (RF-IA-003 corregido) |
| ProbabilidadesIA | JSON {nivel: prob} | Sí | Sistema |
| NivelAsignadoProfesional | Catálogo I–V | Sí | Profesional (nunca autocompletado) |
| Concordancia | Booleano (calculado) | Sí | Sistema (`NivelSugeridoIA == NivelAsignadoProfesional`) |
| MotivoDiscrepancia | Texto / catálogo | Solo si Concordancia = No | Profesional |
| VersionModeloUsado | Texto (ref. ENT-009) | Sí | Sistema |

## Notas de diseño
- Compatible con RNA-002 (nivel + probabilidad + confianza + versión) y RF-TRI-004 (reclasificación como evento separado).
- La reclasificación posterior no se confunde con el registro inicial de concordancia.
- El esquema habilita los reportes de RF-013 (matriz de confusión IA vs. profesional, % concordancia por nivel, listado de discrepancias).
