---
id: 001
slug: fundacion-del-sistema
tipo: epica
prioridad: Must-Have
orden: 1
dependencias: ninguna
bloquea_a: E2, E4, E5, E6
fecha: 2026-07-19
---

# ÉPICA 1 — Fundación del Sistema

## Necesidad de Negocio

Establecer la base técnica, de seguridad y de modelo de datos sobre la cual se construirán todos los demás módulos del sistema de triaje. Sin esta fundación, ningún otro componente puede operar: no hay autenticación, no hay modelo de datos compartido, no hay stack decidido ni entorno de despliegue definido.

## Justificación

El sistema maneja datos clínicos sensibles de pacientes colombianos. La Ley 1581 de 2012 exige protección de datos desde el diseño (privacy by design). Arrancar el desarrollo sin autenticación, roles, cifrado y un modelo de dominio validado generaría retrabajo masivo y riesgo legal.

## Actores

| Rol | Tipo | Responsabilidad |
|-----|------|-----------------|
| Administrador del Sistema | Ejecutor | Configurar roles, usuarios, entorno de despliegue |
| Arquitecto de Software | Aprobador | Validar stack, modelo de dominio, decisiones de arquitectura |
| Todos los usuarios | Beneficiario | Autenticación y acceso según su rol |

## Alcance

- ✅ IN SCOPE:
  - Login/logout con hash de contraseñas (bcrypt/scrypt)
  - Roles RBAC: Administrador, Médico, Enfermera, Investigador, Auditor
  - TLS (HTTPS obligatorio), cifrado en reposo (AES-256)
  - Modelo de dominio completo (ENT-001 a ENT-012) con relaciones
  - Stack tecnológico definido: Python 3.10+, scikit-learn, XGBoost, TensorFlow/PyTorch, Streamlit/Flask, SQLite
  - App demo autocontenida (un solo comando de arranque)
  - Arquitectura modular con configuración externalizada
  - Puntos de extensión documentados para HCE y sistemas hospitalarios
  - Catálogos parametrizables por IPS

- ❌ OUT OF SCOPE:
  - Integración real con LDAP/Active Directory (la demo usa autenticación propia)
  - Integración real con Historia Clínica Electrónica (solo puntos de extensión)
  - Alta disponibilidad productiva (la demo corre en una sola instancia)
  - Cifrado de datos en reposo para datos sintéticos de la demo

## Criterios de Aceptación

```
DADO que el sistema está recién inicializado
CUANDO un usuario intenta acceder a cualquier pantalla sin autenticarse
ENTONCES es redirigido al Login y no puede ver ningún dato clínico

DADO que el Administrador configura los roles del sistema
CUANDO un usuario con rol "Enfermera" inicia sesión
ENTONCES solo ve las pantallas asignadas a su rol (no ve Gestión de Modelos ni Auditoría)

DADO que existe comunicación entre el frontend y el backend
CUANDO se transmite cualquier dato
ENTONCES la conexión usa TLS (HTTPS) sin excepción

DADO que el modelo de dominio está definido
CUANDO se crea un nuevo evento de triaje
ENTONCES todas las entidades relacionadas (Paciente, SignosVitales, EvaluacionClinica) respetan las reglas de integridad y cardinalidad definidas en RD-002
```

## Métricas de Éxito

| Métrica | Línea Base | Meta | Plazo |
|---------|-----------|------|-------|
| Tiempo de setup para nuevo desarrollador | No existe | < 30 min (clone + instalar dependencias + ejecutar) | Antes de iniciar E2 |
| Cobertura de roles en la demo | 0 | 5 roles funcionales (Admin, Médico, Enfermera, Investigador, Auditor) | Cierre de E1 |
| Pantallas protegidas por autenticación | 0 | 12/12 pantallas requieren login | Cierre de E1 |

## Prioridad (MoSCoW)

- **Must Have:** Login, roles RBAC, modelo de dominio, stack definido, app autocontenida, TLS
- **Should Have:** Cifrado en reposo, externalización completa de catálogos
- **Could Have:** Integración con directorio institucional, Docker
- **Won't Have (en este alcance):** Integración real con HCE, alta disponibilidad productiva

## Dependencias

- **Ninguna** — esta épica es el foundation block. Todo depende de ella.

## Archivos Janus que cubre

| Archivo | Tipo |
|---|---|
| `RF-SEC-modulo-seguridad.md` | Funcional |
| `RF-INT-modulo-integraciones.md` | Funcional |
| `RT-002-stack-tecnologico-herramientas.md` | Técnico |
| `RT-007-entorno-despliegue-demo.md` | Técnico |
| `RNF-003-seguridad-informacion-proteccion-datos.md` | No funcional |
| `RNF-007-mantenibilidad-extensibilidad.md` | No funcional |
| `RD-002-modelo-dominio-extendido.md` | Diseño |
