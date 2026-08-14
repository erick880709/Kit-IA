# RNF-003: Seguridad de la Información y Protección de Datos

**Tipo:** Requerimiento no funcional
**Categoría:** Seguridad / Cumplimiento normativo
**Fuente:** CONTEXT TRIA.txt — Secciones 33 (RNS-001 a 010), 34 (RNAU-001 a 006), 35 (RNGD-001 a 006); Ley 1581 de 2012

## Descripción
El sistema debe garantizar la confidencialidad, integridad y disponibilidad de los datos clínicos de los pacientes, en cumplimiento de la Ley 1581 de 2012 de protección de datos personales (Colombia) y de las políticas institucionales de tratamiento de información. Esto abarca autenticación, autorización, cifrado en tránsito y reposo, anonimización para datos de entrenamiento y trazabilidad completa de accesos.

## Criterio medible / restricción concreta
- **RNS-001:** Todo acceso al sistema requiere autenticación (usuario + contraseña con hash + salt, o integración con directorio institucional).
- **RNS-002:** Toda comunicación cliente-servidor utiliza TLS (HTTPS obligatorio, no se acepta HTTP).
- **RNS-003:** Los datos sensibles (identificadores de pacientes, datos clínicos) deben cifrarse en reposo (AES-256 o equivalente).
- **RNS-004 / RNS-005:** Control de acceso basado en roles (RBAC) con principio de mínimo privilegio.
- **RNS-006:** Las contraseñas nunca se almacenan en texto plano (bcrypt/scrypt/PBKDF2 con salt).
- **RNS-007:** Sesiones inactivas expiran automáticamente (tiempo configurable, recomendado ≤ 30 minutos para entorno clínico).
- **RNS-009 / RNS-010:** Cumplimiento Ley 1581 de 2012 — anonimización de datos antes de cualquier uso en entrenamiento; eliminación de identificadores directos (nombre, documento, dirección); transformación de identificadores indirectos.
- **RNAU-003:** Los registros de auditoría son inmutables (append-only, no se permite eliminación).
- **RNGD-006:** Toda modificación estructural del modelo de datos requiere control de cambios documentado.

## Impacto en la arquitectura
- TLS terminado en el servidor de aplicación o en un proxy reverso (Nginx).
- Cifrado en reposo puede delegarse al motor de base de datos o implementarse a nivel de aplicación para campos específicos.
- La anonimización debe implementarse como un paso explícito y auditable en el pipeline de datos, no como una transformación ad-hoc.
- Los logs de auditoría deben almacenarse en un storage separado con políticas de retención y protección contra escritura/eliminación.

## Notas del analista
- Para la demo TFM, el cumplimiento total de Ley 1581 no es exigible (no se despliega en producción con datos reales de pacientes), pero la arquitectura debe documentar cómo se cumpliría. Usar datos sintéticos o anonimizados para la demo.
- La anonimización es el prerrequisito más importante: sin ella, los datos del Hospital San Juan de Dios no pueden usarse ni siquiera para investigación (Art. 2.7 Reglamento UNIR).
