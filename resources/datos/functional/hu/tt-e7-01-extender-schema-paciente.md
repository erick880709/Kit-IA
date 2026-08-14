---
id: TT-E7-01
type: Tarea Técnica
epic: E7 — Datos Ampliados del Paciente
priority: Alta
points: 3
---

# TT-E7-01: Extender esquema BD — nuevos campos en tabla Paciente

## Descripción
Agregar 9 columnas nuevas a la tabla `Paciente` en el schema SQL de `database.py`:
`Nombres`, `Apellidos`, `Telefono`, `Correo`, `ContactoEmergencia`, `NumeroContactoEmergencia`, `Departamento`, `Ciudad`, `DireccionResidencia`.

También crear el catálogo de departamentos y ciudades de Colombia como datos semilla para los dropdowns del formulario.

## Criterios de Done
- [ ] Schema SQL actualizado en `database.py` con las 9 columnas nuevas
- [ ] Constraints CHECK agregados donde aplique (longitud mínima, formato teléfono)
- [ ] Catálogo completo de los **32 departamentos de Colombia** creado como constante `DEPARTAMENTOS_COLOMBIA` en `patient_service.py`
- [ ] Catálogo de **ciudades por departamento** (~200 ciudades) creado como `CIUDADES_POR_DEPARTAMENTO` — el campo Ciudad es una **lista dependiente**: al seleccionar un departamento, solo se muestran las ciudades de ese departamento
- [ ] Índice en `NumeroDocumento` ya existe (verificar)
- [ ] Migración probada: BD existente no pierde datos al agregar columnas (ALTER TABLE ADD COLUMN IF NOT EXISTS)

## Catálogo de Departamentos de Colombia (32)

```python
DEPARTAMENTOS_COLOMBIA = [
    "Amazonas", "Antioquia", "Arauca", "Atlántico", "Bolívar",
    "Boyacá", "Caldas", "Caquetá", "Casanare", "Cauca",
    "Cesar", "Chocó", "Córdoba", "Cundinamarca", "Guainía",
    "Guaviare", "Huila", "La Guajira", "Magdalena", "Meta",
    "Nariño", "Norte de Santander", "Putumayo", "Quindío",
    "Risaralda", "San Andrés y Providencia", "Santander", "Sucre",
    "Tolima", "Valle del Cauca", "Vaupés", "Vichada",
]
```

## Catálogo de Ciudades por Departamento (principales)

Cada departamento lista sus ciudades principales (3-8 por departamento, ~200 en total). La UI muestra solo las ciudades del departamento seleccionado.

```python
CIUDADES_POR_DEPARTAMENTO = {
    "Amazonas": ["Leticia", "Puerto Nariño", "La Chorrera"],
    "Antioquia": ["Medellín", "Bello", "Envigado", "Itagüí", "Rionegro", "Apartadó", "Turbo", "Caucasia"],
    "Arauca": ["Arauca", "Saravena", "Tame", "Arauquita"],
    "Atlántico": ["Barranquilla", "Soledad", "Malambo", "Puerto Colombia", "Sabanalarga"],
    "Bolívar": ["Cartagena", "Magangué", "Turbaco", "El Carmen de Bolívar", "Mompox"],
    "Boyacá": ["Tunja", "Duitama", "Sogamoso", "Chiquinquirá", "Paipa"],
    "Caldas": ["Manizales", "La Dorada", "Villamaría", "Chinchiná", "Riosucio"],
    "Caquetá": ["Florencia", "San Vicente del Caguán", "Cartagena del Chairá"],
    "Casanare": ["Yopal", "Aguazul", "Villanueva", "Paz de Ariporo"],
    "Cauca": ["Popayán", "Santander de Quilichao", "Puerto Tejada", "El Tambo"],
    "Cesar": ["Valledupar", "Aguachica", "Codazzi", "Bosconia", "Curumaní"],
    "Chocó": ["Quibdó", "Istmina", "Bahía Solano", "Nuquí"],
    "Córdoba": ["Montería", "Lorica", "Cereté", "Sahagún", "Planeta Rica"],
    "Cundinamarca": ["Bogotá D.C.", "Soacha", "Facatativá", "Zipaquirá", "Girardot", "Fusagasugá", "Chía", "Mosquera"],
    "Guainía": ["Inírida", "Barranco Minas"],
    "Guaviare": ["San José del Guaviare", "El Retorno", "Calamar"],
    "Huila": ["Neiva", "Pitalito", "Garzón", "La Plata", "Campoalegre"],
    "La Guajira": ["Riohacha", "Maicao", "Uribia", "San Juan del Cesar", "Fonseca"],
    "Magdalena": ["Santa Marta", "Ciénaga", "Fundación", "El Banco", "Aracataca"],
    "Meta": ["Villavicencio", "Acacías", "Granada", "Puerto López", "San Martín"],
    "Nariño": ["Pasto", "Tumaco", "Ipiales", "La Unión", "Túquerres"],
    "Norte de Santander": ["Cúcuta", "Ocaña", "Pamplona", "Villa del Rosario", "Los Patios"],
    "Putumayo": ["Mocoa", "Puerto Asís", "Orito", "Valle del Guamuez"],
    "Quindío": ["Armenia", "Calarcá", "La Tebaida", "Montenegro", "Quimbaya"],
    "Risaralda": ["Pereira", "Dosquebradas", "Santa Rosa de Cabal", "La Virginia"],
    "San Andrés y Providencia": ["San Andrés", "Providencia"],
    "Santander": ["Bucaramanga", "Floridablanca", "Barrancabermeja", "Girón", "Piedecuesta", "San Gil"],
    "Sucre": ["Sincelejo", "Corozal", "San Marcos", "Tolú", "Sincé"],
    "Tolima": ["Ibagué", "Espinal", "Melgar", "Honda", "Mariquita", "Chaparral"],
    "Valle del Cauca": ["Cali", "Palmira", "Buenaventura", "Tuluá", "Cartago", "Buga", "Jamundí", "Yumbo"],
    "Vaupés": ["Mitú", "Carurú"],
    "Vichada": ["Puerto Carreño", "Cumaribo", "La Primavera"],
}
```

## Recurso de datos involucrado

### Recurso
- **Nombre:** Paciente (extensión de schema)
- **Capa(s):** backend (base de datos)

### Campos del recurso (nuevos)
| Campo | Tipo SQLite | Requerido | Descripción / Restricciones |
|---|---|---|---|
| Nombres | TEXT | NOT NULL DEFAULT '' | CHECK(length(Nombres) >= 2) |
| Apellidos | TEXT | NOT NULL DEFAULT '' | CHECK(length(Apellidos) >= 2) |
| Telefono | TEXT | NOT NULL DEFAULT '' | CHECK(length(Telefono) >= 10) |
| Correo | TEXT | — | Sin restricción (opcional) |
| ContactoEmergencia | TEXT | NOT NULL DEFAULT '' | Nombre del contacto |
| NumeroContactoEmergencia | TEXT | NOT NULL DEFAULT '' | CHECK(length(NumeroContactoEmergencia) >= 10) |
| Departamento | TEXT | NOT NULL DEFAULT '' | CHECK(Departamento IN (catálogo 32 deptos)) |
| Ciudad | TEXT | NOT NULL DEFAULT '' | Ciudad/municipio |
| DireccionResidencia | TEXT | NOT NULL DEFAULT '' | CHECK(length(DireccionResidencia) >= 5) |

## Dependencias
- TT-E1-02 (Configurar BD y modelo de dominio) — completada ✅

## Subtareas
- [ ] Escribir ALTER TABLE ADD COLUMN para cada campo nuevo
- [ ] Crear diccionario DEPARTAMENTOS_COLOMBIA con los 32 departamentos
- [ ] Crear diccionario CIUDADES_POR_DEPARTAMENTO con ciudades principales
- [ ] Agregar índices si son necesarios para búsqueda por departamento/ciudad
