---
id: HU-E1-01
type: Historia de Usuario
epic: 001-fundacion-del-sistema
priority: Alta
points: 3
---

# HU-E1-01: Login de Usuarios

## Como
Usuario del sistema (cualquier rol)

## Quiero
Iniciar sesión con mi usuario y contraseña

## Para
Acceder a las funcionalidades del sistema según mi rol asignado

## Criterios de Aceptación
- [ ] CA1: La pantalla de login solicita usuario y contraseña con campos obligatorios
- [ ] CA2: Las credenciales se validan contra la base de datos (contraseña hasheada con bcrypt + salt)
- [ ] CA3: Si las credenciales son correctas, el usuario accede al sistema y ve solo las pantallas de su rol
- [ ] CA4: Si las credenciales son incorrectas, se muestra mensaje de error genérico (sin revelar si falló usuario o contraseña)
- [ ] CA5: Tras 5 intentos fallidos consecutivos, la cuenta se bloquea temporalmente (15 min)

## Recurso de datos involucrado
- **Nombre:** Usuario
- **Capa(s):** backend + frontend

### Campos del recurso
| Campo | Tipo | Requerido | Descripción / Restricciones |
|---|---|---|---|
| IdUsuario | UUID | Sí | Identificador único |
| NombreUsuario | Texto | Sí | Unique, alfanumérico, min 4 caracteres |
| PasswordHash | Texto | Sí | bcrypt + salt, nunca en texto plano |
| Rol | Catálogo | Sí | Administrador / Médico / Enfermera / Investigador / Auditor |
| Activo | Booleano | Sí | Default true |
| IntentosFallidos | Entero | Sí | Default 0, se resetea al iniciar sesión correctamente |
| BloqueadoHasta | DateTime | No | Se establece tras 5 intentos fallidos |
| FechaCreacion | DateTime | Sí | Automático |

## Subtareas
- [ ] Diseñar pantalla de login (Streamlit)
- [ ] Implementar endpoint de autenticación (bcrypt + salt)
- [ ] Implementar bloqueo por intentos fallidos
- [ ] Conectar frontend con backend de autenticación
