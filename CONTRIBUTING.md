# Contribuir a Kit IA

¡Gracias por tu interés en contribuir! Kit IA es un proyecto abierto que crece con el aporte de la comunidad.

## Cómo contribuir

### 🐛 Reportar bugs

1. Usá el [issue tracker](https://github.com/erick880709/Kit-IA/issues)
2. Describí el bug con: qué skill falló, qué esperabas que pasara, qué pasó en realidad
3. Si es posible, incluí la conversación o prompt que disparó el error

### 💡 Proponer mejoras

1. Abrí un issue con la etiqueta `enhancement`
2. Describí el skill nuevo o la mejora propuesta
3. Explicá dónde encajaría en el pipeline (fase del `orquestador`)

### 🔧 Agregar un skill nuevo

Cada skill es una carpeta en `.github/skills/` con esta estructura:

```
.github/skills/mi-skill/
├── SKILL.md              # Instrucciones del skill (obligatorio)
└── references/           # Archivos de referencia (opcional)
    └── guia-ejemplo.md
```

**Estructura de `SKILL.md`:**

```yaml
---
name: mi-skill
description: >
  Descripción concisa de lo que hace el skill, con triggers (palabras clave)
  que lo activan. Úsala cuando el usuario pida "hacer X", "generar Y".
---
# Título del Skill

## Propósito
...

## Pasos
...
```

**Reglas:**
- El `name` en YAML debe coincidir con el nombre de la carpeta
- La `description` debe incluir palabras clave de activación (triggers) en español
- Si tu skill necesita referencias, creá la carpeta `references/` dentro
- Si tu skill es parte del pipeline, actualizá `orquestador/SKILL.md` con:
  - Una rama en el árbol de decisión
  - La entrada en la secuencia completa
  - La carpeta en el contrato `resources/` si escribe/lee datos

### 📝 Estándares de código

- **Idioma:** Skills en español con triggers claros. Referencias técnicas pueden usar términos en inglés donde sea estándar (CQRS, TDD, etc.)
- **Formato:** Markdown con frontmatter YAML
- **Tono:** Profesional, directo, sin relleno. Cada skill debe ser accionable por un asistente de IA.

## Proceso de Pull Request

1. Hacé un fork del repo
2. Creá una rama: `git checkout -b feature/mi-skill`
3. Agregá tus cambios: `git add .github/skills/mi-skill/`
4. Commiteá: `git commit -m "Agrega skill: mi-skill"`
5. Pusheá: `git push origin feature/mi-skill`
6. Abrí un PR contra `main`

## Código de conducta

- Sé respetuoso y constructivo
- Los debates técnicos son bienvenidos; los ataques personales no
- Este es un proyecto para que equipos reales desarrollen mejor — mantenelo práctico

---

Gracias por construir con nosotros. 🧠
