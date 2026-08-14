# Documento Consolidado de Cambios Pendientes

**Versión:** 1.0 · **Fecha:** 2026-07-19 · **Proyecto:** TFM UNIR · **Sistema:** Triaje Multimodal IA

> **Objetivo:** Centralizar todos los cambios solicitados que están pendientes de implementación para que el equipo de desarrollo pueda ejecutarlos en orden, con trazabilidad completa de cada modificación.

---

## 📊 Resumen Ejecutivo

| Épica | ID | Tipo | Título | Prioridad | Puntos |
|---|---|---|---|---|---|
| E7 | TT-E7-01 | Tarea Técnica | Extender schema BD con 9 campos nuevos en Paciente | 🔴 Alta | 3 |
| E7 | TT-E7-02 | Tarea Técnica | Actualizar PatientService con nuevos campos y validaciones | 🔴 Alta | 3 |
| E7 | TT-E7-03 | Tarea Técnica | Actualizar UI de registro de paciente con nuevos campos | 🔴 Alta | 5 |
| E7 | HU-E7-01 | Historia de Usuario | Registrar datos personales completos del paciente | 🔴 Alta | 5 |
| **TOTAL** | **4 issues** | | | | **16 SP** |

### Orden de ejecución recomendado

```
TT-E7-01 (Schema BD)
    ↓
TT-E7-02 (PatientService)
    ↓
TT-E7-03 (UI Paciente)
    ↓
HU-E7-01 (Verificación E2E)
```

---

## 🔍 Detalle de Cambios

### Cambio 1: Nuevos campos en tabla Paciente

**Archivo:** `sistema-triaje-ia/app/data/database.py`

Se deben agregar 9 columnas a la tabla `Paciente`:

```sql
ALTER TABLE Paciente ADD COLUMN Nombres TEXT NOT NULL DEFAULT '';
ALTER TABLE Paciente ADD COLUMN Apellidos TEXT NOT NULL DEFAULT '';
ALTER TABLE Paciente ADD COLUMN Telefono TEXT NOT NULL DEFAULT '';
ALTER TABLE Paciente ADD COLUMN Correo TEXT;
ALTER TABLE Paciente ADD COLUMN ContactoEmergencia TEXT NOT NULL DEFAULT '';
ALTER TABLE Paciente ADD COLUMN NumeroContactoEmergencia TEXT NOT NULL DEFAULT '';
ALTER TABLE Paciente ADD COLUMN Departamento TEXT NOT NULL DEFAULT '';
ALTER TABLE Paciente ADD COLUMN Ciudad TEXT NOT NULL DEFAULT '';
ALTER TABLE Paciente ADD COLUMN DireccionResidencia TEXT NOT NULL DEFAULT '';
```

**Catálogos nuevos requeridos:**

- `DEPARTAMENTOS_COLOMBIA`: lista con los **32 departamentos** de Colombia
- `CIUDADES_POR_DEPARTAMENTO`: dict con **~200 ciudades** mapeadas por departamento
- **Mecanismo dependiente:** `Ciudad` es un dropdown que se filtra automáticamente según el `Departamento` seleccionado

```
DEPARTAMENTOS_COLOMBIA = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar",
    "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca",
    "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía",
    "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta",
    "Nariño", "Norte de Santander", "Putumayo", "Quindío",
    "Risaralda", "San Andrés y Providencia", "Santander", "Sucre",
    "Tolima", "Valle del Cauca", "Vaupés", "Vichada",
]

CIUDADES_POR_DEPARTAMENTO = {
    "Antioquia": ["Medellín", "Bello", "Envigado", "Itagüí", "Rionegro", "Apartadó", "Turbo", "Caucasia"],
    "Atlántico": ["Barranquilla", "Soledad", "Malambo", "Puerto Colombia", "Sabanalarga"],
    "Cundinamarca": ["Bogotá D.C.", "Soacha", "Facatativá", "Zipaquirá", "Girardot", "Fusagasugá", "Chía", "Mosquera"],
    "Valle del Cauca": ["Cali", "Palmira", "Buenaventura", "Tuluá", "Cartago", "Buga", "Jamundí", "Yumbo"],
    "Santander": ["Bucaramanga", "Floridablanca", "Barrancabermeja", "Girón", "Piedecuesta", "San Gil"],
    # ... (32 departamentos, ~200 ciudades en total)
}
```

### Cambio 2: Validaciones en PatientService

**Archivo:** `sistema-triaje-ia/app/services/patient_service.py`

- `register_patient()` acepta 9 parámetros nuevos
- `_validar_telefono()`: mínimo 10 dígitos, acepta +57
- `_validar_correo()`: contiene @ y . si no está vacío
- `search_patients()`: búsqueda por nombre y apellidos
- `ControlCambios`: registro automático al modificar cualquier campo

### Cambio 3: UI del formulario de paciente

**Archivo:** `sistema-triaje-ia/app/ui/patient_page.py`

Nuevo layout del formulario organizado en 4 secciones:

1. **Datos Personales:** Nombres, Apellidos, Tipo Doc, Núm Doc, Fecha Nac, Sexo
2. **Contacto:** Teléfono, Correo
3. **Contacto de Emergencia:** Nombre, Teléfono
4. **Residencia:** Departamento (dropdown), Ciudad (dropdown dinámico), Dirección

### Cambio 4: Flujo E2E de registro

**Archivos:** `patient_page.py`, `vital_signs_page.py`, `clinical_eval_page.py`, `triage_validation_page.py`

- En todas las pantallas del flujo, mostrar Nombres y Apellidos junto al documento
- En el reporte HTML de triaje, incluir datos de contacto y residencia (anonimizados)
- En la búsqueda de pacientes, permitir buscar por nombre o apellidos

---

## 📋 Checklist de Implementación

### Fase 1: Base de Datos (TT-E7-01)
- [ ] Agregar 9 ALTER TABLE a `database.py`
- [ ] Crear catálogo `DEPARTAMENTOS_COLOMBIA`
- [ ] Crear catálogo `CIUDADES_POR_DEPARTAMENTO`
- [ ] Verificar migración no destructiva

### Fase 2: Servicio (TT-E7-02)
- [ ] Actualizar firma de `register_patient()`
- [ ] Implementar `_validar_telefono()`
- [ ] Implementar `_validar_correo()`
- [ ] Actualizar INSERT SQL
- [ ] Actualizar `search_patients()` con búsqueda por nombre
- [ ] Integrar `registrar_cambio()` en modificaciones

### Fase 3: UI (TT-E7-03)
- [ ] Rediseñar layout del formulario (4 secciones)
- [ ] Agregar dropdowns Departamento → Ciudad
- [ ] Validación client-side teléfono/correo
- [ ] Actualizar flujo de duplicados
- [ ] Mostrar nombres en cabeceras de otras pantallas

### Fase 4: Verificación (HU-E7-01)
- [ ] Probar registro con todos los campos
- [ ] Probar validaciones (teléfono inválido, correo sin @)
- [ ] Probar búsqueda por nombre
- [ ] Probar flujo multi-visita con datos completos
- [ ] Verificar ControlCambios registra modificaciones

---

## 🔗 Archivos de Referencia

| Archivo | Descripción |
|---|---|
| `resources/functional/hu/hu-e7-01-datos-personales-paciente.md` | Historia de usuario completa |
| `resources/functional/hu/tt-e7-01-extender-schema-paciente.md` | Tarea técnica: BD |
| `resources/functional/hu/tt-e7-02-actualizar-patient-service.md` | Tarea técnica: Servicio |
| `resources/functional/hu/tt-e7-03-actualizar-ui-paciente.md` | Tarea técnica: UI |

---

## ⚠️ Riesgos y Consideraciones

1. **Migración no destructiva:** Usar `ALTER TABLE ADD COLUMN IF NOT EXISTS` o verificar si la columna ya existe antes de agregarla
2. **Datos existentes:** Los registros de pacientes ya creados tendrán strings vacíos en los nuevos campos
3. **Rendimiento:** Los dropdowns de departamento/ciudad son datos estáticos — no requieren consultas a BD
4. **Internacionalización:** El catálogo de departamentos es específico de Colombia (32 departamentos)
5. **Privacidad:** El correo y teléfono son datos personales — aplicar anonimización en exportaciones (Ley 1581/2012)
