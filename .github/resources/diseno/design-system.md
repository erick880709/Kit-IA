# Design System — TriajeIA

**Fuente:** `design-system/triajeia/MASTER.md` (generado por ui-ux-pro-max con query "healthcare clinical triage dashboard", densidad 8, varianza 3)

## Paleta

| Token | Hex | Uso en la demo |
|---|---|---|
| Primary | `#0891B2` | Acciones principales, header |
| Secondary | `#22D3EE` | Elementos secundarios, info |
| Accent/CTA | `#059669` | Botones de confirmación/éxito |
| Background | `#ECFEFF` | Fondo de pantallas |
| Foreground | `#164E63` | Texto principal |
| Muted | `#E8F1F6` | Superficies secundarias |
| Border | `#A5F3FC` | Bordes y separadores |
| Destructive | `#DC2626` | Errores, alertas críticas |
| Warning (derivado) | `#F59E0B` | Discrepancias, alertas |

**Nota:** "Calm cyan + health green" — apto para entorno clínico (no neon, sin gradientes IA).

## Tipografía

- **Familia:** Fira Sans (texto) + Fira Code (datos/código)
- Mood: dashboard, data, analítica, técnico, preciso
- Google Fonts: `Fira+Code:wght@400;500;600;700&family=Fira+Sans:wght@300;400;500;600;700`

## Escala de espaciado (wireframes)

- Contenedor de pantalla: padding 30px
- Separación entre campos: 32px
- Botón CTA: alto 48-56px, radio 8px

## Reglas de UI (checklist del sistema)

- Sin emojis como iconos (usar SVG: Heroicons/Lucide)
- `cursor-pointer` en todo elemento clicable
- Contraste mínimo 4.5:1 en texto (modo claro)
- Focus visible para navegación por teclado
- Respetar `prefers-reduced-motion`

## Mapeo a Excalidraw (wireframes)

| Token | Color Excalidraw |
|---|---|
| Primary #0891B2 | Cyan `#06b6d4` |
| Accent #059669 | Green `#22c55e` / Light Green `#b2f2bb` |
| Background #ECFEFF | Light Teal `#c3fae8` |
| Border #A5F3FC | Light Blue `#a5d8ff` |
| Destructive #DC2626 | Red `#ef4444` / Light Red `#ffc9c9` |
| Warning | Amber `#f59e0b` / Light Yellow `#fff3bf` |
| Destacado IA | Light Purple `#d0bfff` |
