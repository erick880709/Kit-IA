---
id: HU-E2-01
type: Historia de Usuario
epic: 002-flujo-clinico-triaje
priority: Alta
points: 5
---

# HU-E2-01: Registrar Nuevo Paciente

## Como
Personal Administrativo

## Quiero
Registrar un nuevo paciente que ingresa al servicio de urgencias con sus datos básicos, vía de llegada y búsqueda automática de duplicados

## Para
Iniciar el episodio de atención y crear el evento de triaje asociado

## Criterios de Aceptación
- [ ] CA1: Formulario con campos: TipoDocumento (catálogo), NumeroDocumento, FechaNacimiento, Sexo (catálogo), RégimenSalud, EPS, Municipio, ViaLlegada (catálogo: Ambulancia/Particular/Remisión)
- [ ] CA2: Al perder el foco del campo NumeroDocumento, el sistema busca duplicados y alerta si el paciente ya existe
- [ ] CA3: Si el paciente ya existe, se recuperan sus datos demográficos y se muestra su historial de episodios previos (EpisodiosPreviosUrgencias)
- [ ] CA4: Al guardar, se genera un UUID de episodio, se registra fecha/hora de ingreso automática y se crea el evento de triaje en estado "Registrado"
- [ ] CA5: Validación en tiempo real de campos obligatorios (TipoDocumento, NumeroDocumento, FechaNacimiento, Sexo, ViaLlegada) y formatos
- [ ] CA6: La edad se calcula automáticamente a partir de FechaNacimiento

## Recurso de datos involucrado
- **Nombre:** Paciente (ENT-001 extendido)
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdPaciente | UUID | Sí | Generado automáticamente |
| TipoDocumento | Catálogo | Sí | CC, TI, CE, PA, RC |
| NumeroDocumento | Texto | Sí | Alfanumérico, unique |
| FechaNacimiento | Fecha | Sí | Formato YYYY-MM-DD |
| Edad | Entero | Sí | Calculado automáticamente |
| Sexo | Catálogo | Sí | M, F |
| RegimenSalud | Catálogo | No | Contributivo, Subsidiado, Especial, No afiliado |
| EPS | Texto | No | Nombre de la EPS |
| Municipio | Texto | No | Municipio de residencia |
| ViaLlegada | Catálogo | Sí | Ambulancia, Particular, Remisión |
| EpisodiosPreviosUrgencias | Entero | No | Calculado/consultado del historial |

### Relaciones con otros recursos
- `EventoTriaje` (1:N): cada registro de paciente puede tener múltiples eventos

## Subtareas
- [ ] Diseñar pantalla de Registro de Paciente
- [ ] Implementar búsqueda de duplicados en tiempo real
- [ ] Implementar creación del evento de triaje asociado
- [ ] Implementar validación de campos obligatorios y formatos
- [ ] Conectar con catálogo de Vía de Llegada
