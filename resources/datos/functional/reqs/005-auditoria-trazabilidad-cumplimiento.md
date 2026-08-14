---
id: 005
slug: auditoria-trazabilidad-cumplimiento
tipo: epica
prioridad: Should-Have
orden: 4
dependencias: E1
se_integra_con: E2, E4
fecha: 2026-07-19
---

# ÉPICA 5 — Auditoría, Trazabilidad y Cumplimiento

## Necesidad de Negocio

Garantizar que cada acción sobre el sistema — desde el registro de un paciente hasta el cierre de un evento de triaje, pasando por cada ejecución de IA y cada validación del profesional — quede registrada de forma inmutable, trazable y auditable. La auditoría no es opcional: es un requisito normativo colombiano (Resolución 5596/2015 exige trazabilidad del triaje) y un habilitador para la detección de deriva del modelo y la comparativa IA vs. profesional.

## Justificación

Sin trazabilidad, el sistema no puede demostrar que la IA apoyó (no reemplazó) al profesional. Sin auditoría, no hay forma de medir la concordancia IA vs. profesional (RF-REP-005), ni de detectar degradación del modelo (RNA-010), ni de cumplir con la Ley 1581 de 2012 en cuanto a responsabilidad sobre los datos. La auditoría es el "sistema nervioso" que registra todo lo que ocurre.

## Actores

| Rol | Tipo | Responsabilidad |
|-----|------|-----------------|
| Auditor | Beneficiario / Ejecutor | Consultar y exportar registros de auditoría |
| Sistema | Ejecutor | Registrar automáticamente cada acción |
| Administrador | Soporte | Configurar políticas de retención |

## Alcance

- ✅ IN SCOPE:
  - Registro automático e inmutable de toda acción: creación de paciente, signos vitales, evaluación, ejecución IA, validación, reclasificación, cierre, login/logout
  - Cada registro incluye: usuario, timestamp (UTC), acción, valor anterior/nuevo (si aplica), IP, dispositivo, identificador del evento
  - Almacenamiento append-only (no se permite eliminar registros)
  - Consulta de auditoría con filtros: usuario, paciente, fecha (rango), modelo/versión, tipo de acción, nivel de triaje
  - Resultados paginados y ordenables
  - Exportación: CSV, Excel, PDF
  - Registro de triaje descargable por evento: paciente anonimizado, fecha/hora, nivel IA vs. profesional, signos vitales, motivo, top SHAP
  - Trazabilidad de cada variable: propietario, definición, origen
  - Validación de calidad del dato antes de la inferencia (RNQ-001 a 006)
  - Catálogos controlados centralizados con control de cambios
  - Las modificaciones estructurales del modelo de datos requieren registro de cambio

- ❌ OUT OF SCOPE:
  - Firma digital de registros de auditoría
  - Exportación automática a sistemas externos de compliance
  - Políticas de retención automática (purgado de registros antiguos)
  - Dashboard de auditoría en tiempo real

## Criterios de Aceptación

```
DADO que un usuario modifica un signo vital de un paciente
CUANDO se guarda el cambio
ENTONCES el registro de auditoría contiene: usuario, timestamp, valor anterior, valor nuevo y motivo

DADO que el auditor quiere revisar todas las discrepancias IA vs. profesional del último mes
CUANDO aplica los filtros: tipo_acción = "validación", concordancia = No, fecha = último mes
ENTONCES obtiene un listado con cada caso, niveles asignados, motivo de discrepancia y profesional responsable

DADO que se intenta eliminar un registro de auditoría (API o acceso directo a BD)
CUANDO se ejecuta la operación
ENTONCES el sistema la rechaza (append-only, sin permisos de DELETE en la tabla de auditoría)

DADO que un evento de triaje está cerrado
CUANDO el médico solicita el registro de triaje descargable
ENTONCES el PDF generado contiene: paciente anonimizado, fecha/hora, nivel IA vs. humano, signos vitales, motivo de consulta, top 5 variables SHAP
```

## Métricas de Éxito

| Métrica | Línea Base | Meta | Plazo |
|---------|-----------|------|-------|
| Cobertura de acciones auditadas | 0% | 100% de las acciones definidas en RF-AUD-001 | Cierre de E5 |
| Registros de auditoría inmutables | No existe | 0 eliminaciones posibles (append-only verificado) | Cierre de E5 |
| Consultas de auditoría | No existe | < 1 segundo para búsquedas con hasta 3 filtros simultáneos | Cierre de E5 |
| Formatos de exportación | 0 | 3 formatos funcionales (CSV, Excel, PDF) | Cierre de E5 |

## Prioridad (MoSCoW)

- **Must Have:** Registro automático de acciones principales (inferencia, validación, cambios), consulta con filtros básicos, append-only
- **Should Have:** Exportación CSV/Excel/PDF, registro de triaje descargable, catálogos centralizados
- **Could Have:** Dashboard de auditoría, alertas por patrones sospechosos, integración con sistemas de compliance
- **Won't Have (en este alcance):** Firma digital, blockchain para auditoría, retención automática

## Dependencias

- **E1 (Fundación):** Login, roles (el rol Auditor debe existir), modelo de dominio
- **Se integra con E2 y E4:** Los eventos de auditoría se disparan desde las acciones del flujo clínico y del motor IA

## Archivos Janus que cubre

| Archivo | Tipo |
|---|---|
| `RF-AUD-modulo-auditoria.md` | Funcional |
| `RNF-005-trazabilidad-auditabilidad-gobierno-dato.md` | No funcional |
