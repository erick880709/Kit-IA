---
id: 002
slug: flujo-clinico-triaje
tipo: epica
prioridad: Must-Have
orden: 2
dependencias: E1
bloquea_a: E4
fecha: 2026-07-19
---

# ÉPICA 2 — Flujo Clínico de Triaje

## Necesidad de Negocio

Digitalizar el proceso completo de clasificación de pacientes en urgencias, desde el registro inicial hasta el cierre del evento de triaje, capturando toda la información clínica necesaria (signos vitales, evaluación clínica, motivo de consulta) para que el motor de IA pueda ejecutar la inferencia. Este flujo es el camino crítico del sistema: sin él, no hay datos que alimenten al modelo.

## Justificación

Actualmente el proceso de triaje en Colombia es manual, con alta variabilidad entre profesionales (dos enfermeras pueden clasificar al mismo paciente en niveles distintos) y sin trazabilidad estructurada. Este módulo digitaliza el flujo completo aplicando la Resolución 5596 de 2015, garantizando que los datos se capturen de forma estandarizada y validada antes de llegar al modelo de IA.

## Actores

| Rol | Tipo | Responsabilidad |
|-----|------|-----------------|
| Personal Administrativo | Ejecutor | Registrar paciente, buscar duplicados |
| Enfermera de Triaje | Ejecutor | Capturar signos vitales, evaluación clínica, ejecutar IA, validar clasificación |
| Médico de Urgencias | Beneficiario / Ejecutor | Validar clasificación, reclasificar, consultar historial |
| Paciente | Beneficiario | Recibir clasificación precisa y oportuna |

## Alcance

- ✅ IN SCOPE:
  - 7 pantallas del flujo clínico principal: Login → Registro Paciente → Signos Vitales → Evaluación Clínica → Clasificación IA → Explicación SHAP → Validación
  - Captura de 8 signos vitales con validación de rangos fisiológicos y alertas visuales
  - Evaluación clínica completa: motivo de consulta (texto libre + catálogo), dolor (0-10), Glasgow, conciencia, antecedentes, alergias, observaciones
  - Máquina de estados del triaje: Registrado → En evaluación → Pendiente IA → Clasificado → Validado → Cerrado
  - Reclasificación con motivo obligatorio y preservación del historial
  - Campo `ViaLlegada` (Ambulancia/Particular/Remisión) como catálogo controlado
  - Campo `EpisodiosPreviosUrgencias` en el formulario de antecedentes
  - Búsqueda de pacientes por documento, nombre, historia clínica
  - Cálculo automático de IMC (peso + talla)
  - Validación en tiempo real de campos obligatorios y formatos

- ❌ OUT OF SCOPE:
  - Integración con HCE para consultar antecedentes (los datos se capturan manualmente)
  - Ejecución real del modelo IA (es la Épica 4)
  - Dashboard de indicadores (es la Épica 6)
  - Registros de auditoría (es la Épica 5)

## Criterios de Aceptación

```
DADO que un paciente llega a urgencias
CUANDO el administrativo completa el formulario de registro con datos válidos
ENTONCES se genera un UUID de episodio y un evento de triaje en estado "Registrado"

DADO que la enfermera está capturando signos vitales
CUANDO ingresa una SpO₂ de 105% o una temperatura de 50°C
ENTONCES el sistema muestra una alerta visual y requiere confirmación antes de continuar

DADO que el evento de triaje está en estado "Validado"
CUANDO el médico necesita reclasificar al paciente por cambio en su condición
ENTONCES puede seleccionar un nuevo nivel, debe registrar el motivo, y el nivel anterior se conserva en el historial

DADO que el profesional termina la evaluación clínica
CUANDO todos los campos obligatorios están completos
ENTONCES el botón "Ejecutar IA" se habilita y el evento transiciona a "Pendiente IA"

DADO que la clasificación está completa y validada
CUANDO el profesional intenta cerrar el evento sin haber registrado su propia clasificación (NivelAsignadoProfesional)
ENTONCES el sistema impide el cierre y solicita completar el campo
```

## Métricas de Éxito

| Métrica | Línea Base | Meta | Plazo |
|---------|-----------|------|-------|
| Tiempo para completar un triaje (nuevo paciente) | No existe (proceso manual) | < 5 min desde registro hasta validación | Cierre de E2 |
| Pantallas del flujo principal | 0 | 7 funcionales con navegación completa | Cierre de E2 |
| Cobertura de estados del triaje | 0 | 7 estados con transiciones controladas | Cierre de E2 |
| Campos clínicos capturados | 0 | 100% de los definidos en RF-VIT + RF-EVA | Cierre de E2 |

## Prioridad (MoSCoW)

- **Must Have:** Las 7 pantallas del flujo principal, máquina de estados, validación de signos vitales, captura de todos los campos clínicos, ViaLlegada como catálogo
- **Should Have:** Búsqueda avanzada de pacientes, auto-guardado de evaluaciones parciales
- **Could Have:** Modo offline (sin conexión), carga de signos vitales desde dispositivos médicos
- **Won't Have (en este alcance):** Integración con HCE, firma digital del profesional

## Dependencias

- **E1 (Fundación):** Login, roles, modelo de dominio — sin esto no se puede construir el flujo
- **E4 (Motor IA):** El botón "Ejecutar IA" queda como placeholder hasta integrar E4

## Archivos Janus que cubre

| Archivo | Tipo |
|---|---|
| `RF-PAC-001-registrar-paciente.md` | Funcional |
| `RF-PAC-002-buscar-paciente.md` | Funcional |
| `RF-PAC-003-consultar-historial.md` | Funcional |
| `RF-PAC-004-validacion-datos-paciente.md` | Funcional |
| `RF-TRI-001-crear-evento-triaje.md` | Funcional |
| `RF-TRI-002-registrar-hora-inicio.md` | Funcional |
| `RF-TRI-003-estados-triaje.md` | Funcional |
| `RF-TRI-004-reclasificacion-paciente.md` | Funcional |
| `RF-TRI-005-cierre-evento-triaje.md` | Funcional |
| `RF-VIT-captura-signos-vitales.md` | Funcional |
| `RF-EVA-evaluacion-clinica.md` | Funcional |
| `RD-001-inventario-pantallas-demo.md` | Diseño |
| `RD-003-flujo-clasificacion-ia-validacion.md` | Diseño |
| `RNF-004-usabilidad-entorno-clinico.md` | No funcional |
