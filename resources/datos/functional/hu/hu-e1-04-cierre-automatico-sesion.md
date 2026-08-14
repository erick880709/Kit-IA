---
id: HU-E1-04
type: Historia de Usuario
epic: 001-fundacion-del-sistema
priority: Alta
points: 2
---

# HU-E1-04: Cierre Automático de Sesión por Inactividad

## Como
Usuario del sistema (especialmente en entorno clínico compartido)

## Quiero
Que mi sesión se cierre automáticamente tras un período de inactividad

## Para
Evitar que personal no autorizado acceda a datos clínicos si dejo la estación de trabajo abierta

## Criterios de Aceptación
- [ ] CA1: Tras 15 minutos de inactividad (sin clics ni interacción), la sesión expira automáticamente
- [ ] CA2: El usuario es redirigido a la pantalla de login con un mensaje "Su sesión expiró por inactividad"
- [ ] CA3: El Administrador puede configurar el tiempo de inactividad (entre 5 y 60 minutos)
- [ ] CA4: Si el usuario estaba completando un formulario, los datos no guardados se pierden (se advierte con un contador regresivo 1 minuto antes de la expiración)

## Recurso de datos involucrado
- **Nombre:** Configuración del Sistema
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| TiempoInactividadMinutos | Entero | Sí | Default 15, rango 5-60, configurable por Admin |
| MostrarAvisoPrevio | Booleano | Sí | Default true |

## Subtareas
- [ ] Implementar contador de inactividad en frontend
- [ ] Implementar expiración de sesión en backend
- [ ] Diseñar aviso de expiración inminente (contador regresivo)
- [ ] Crear pantalla de configuración para el Admin
