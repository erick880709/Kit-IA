# Mockups TriajeIA — HTML + JPG

Generados 2026-08-13 por `figma-prd-mockups` (Path B Excalidraw + exportes estáticos).

## Contenido

| Archivo | Descripción |
|---|---|
| `triajeia-mockups.html` | Galería HTML con las 9 vistas estilizadas según el design system TriajeIA (`.github/resources/diseno/design-system.md`). Abrir en navegador para revisión interactiva. |
| `jpg/01-login.jpg` … `09-flujo-clinico.jpg` | Exportes JPG por sección (quality 90) para presentaciones y anexos del TFM. |

## Cómo regenerar los JPG

1. Abrir `triajeia-mockups.html` en un navegador (o con el navegador integrado de VS Code).
2. Capturar cada `<section id="s-*">` con una herramienta de screenshot (Playwright, DevTools "Capture node screenshot", etc.) en formato JPEG.

## Correspondencia con las vistas Excalidraw

| JPG | Sección HTML | Vista Excalidraw (checkpoint) |
|---|---|---|
| 01-login | `#s-login` | `94bf80065d6a4dc8b4` |
| 02-registro-paciente | `#s-registro` | `9bd8e837eb4e464fad` |
| 03-signos-vitales | `#s-signos` | `4dbfe99b0bdb4ebea3` |
| 04-evaluacion-clinica | `#s-evaluacion` | `7f43bdba4f274c11b6` |
| 05-clasificacion-ia | `#s-clasificacion` | `3b8da5b846da457c99` |
| 06-explicacion-shap | `#s-shap` | `ee0c01ad72d14c63ba` |
| 07-validacion-discrepancia | `#s-validacion` | `4c5ae301e2b348f885` |
| 08-cierre-evento | `#s-cierre` | `67afce8580bc4109b1` |
| 09-flujo-clinico | `#s-flujo` | `1c4392b150924a6bb8` |

## Design system aplicado

- Paleta: Primary `#0891B2` · Accent `#059669` · Background `#ECFEFF` · Foreground `#164E63` · Destructive `#DC2626` · Warning `#F59E0B`
- Tipografía: Fira Sans (texto) + Fira Code (datos), vía Google Fonts con fallback `system-ui`.
- Densidad 8, varianza 3 — "Calm cyan + health green" (entorno clínico, sin gradientes neon).
