---
id: TT-E1-03
type: Tarea Técnica
epic: 001-fundacion-del-sistema
priority: Alta
points: 3
---

# TT-E1-03: Implementar TLS/HTTPS y Cifrado en Reposo

## Descripción
Configurar la capa de seguridad en tránsito (TLS para HTTPS) y documentar la estrategia de cifrado en reposo para datos sensibles, en cumplimiento de la Ley 1581 de 2012 y RNS-002/RNS-003.

## Criterios de Done
- [ ] Para desarrollo local: Streamlit configurado con certificado autofirmado (o documentar que en dev se usa HTTP y en prod se pondría detrás de Nginx con TLS)
- [ ] Documentación de cómo se configuraría TLS en producción (Nginx reverse proxy + Let's Encrypt)
- [ ] Campos sensibles identificados en el modelo de datos (NumeroDocumento, Nombre en textos clínicos)
- [ ] Estrategia de cifrado en reposo documentada (AES-256 a nivel de aplicación para campos específicos, o TDE del motor de BD)
- [ ] Nota explícita en README: "Los datos de la demo son sintéticos — el cifrado en reposo no se activa en desarrollo pero está documentado para producción"

## Dependencias
TT-E1-01 (proyecto inicializado)

## Subtareas
- [ ] Configurar HTTPS local con certificado autofirmado (o documentar decisión de usar HTTP en dev)
- [ ] Redactar documento de estrategia de cifrado en reposo
- [ ] Marcar campos sensibles en el esquema de BD
