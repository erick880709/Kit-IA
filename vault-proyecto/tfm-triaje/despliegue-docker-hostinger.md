---
fecha: 2026-08-14
tags: [tfm, triaje, despliegue, docker, hostinger, ops]
proyecto: TFM Triaje IA UNIR
fase: entrega
origen: "[[tfm-triaje/evidencia-ingenieria]]"
---

# Despliegue Docker + Hostinger

## Imagen Docker

- `Dockerfile` (python:3.11-slim, usuario sin privilegios, HEALTHCHECK
  `/_stcore/health`), `docker-entrypoint.sh` (seed idempotente + arranque con
  `python -m streamlit`), `docker-compose.yml` (volúmenes data/logs).
- Imagen **`triaje-ia:demo`** (2,62 GB) construida y verificada: contenedor
  healthy, login OK en `localhost:8502`.
- Los datasets clínicos NUNCA entran a la imagen (`.dockerignore`).

## Hostinger — producto recomendado

| Plan | vCPU | RAM | NVMe | Precio promo (2 años) |
|---|---|---|---|---|
| KVM 1 | 1 | 4 GB | 50 GB | $6.49/mes |
| **KVM 2 ✔** | **2** | **8 GB** | **100 GB** | **$8.79/mes** |
| KVM 4 | 4 | 16 GB | 200 GB | $12.99/mes |

- **Descartar** hosting compartido/cloud (no admite Docker ni puertos propios).
- Adquirir: KVM 2 por 24 meses + Ubuntu 24.04 con Docker de un clic + dominio
  gratis 1 año + datacenter São Paulo (mejor latencia desde Colombia).
- Pasos y comandos: `resources/engineering/release/despliegue-hostinger.md`.

## Demo gratuita antes del VPS

- GitHub Pages ❌ (solo estático); Codespaces ⚠ temporal; **Streamlit
  Community Cloud ✅** (HTTPS, 1 clic) y **HF Spaces CPU Basic ✅**
  (2 vCPU/16 GB gratis, shim `app.py` listo); Oracle Always Free ⚠ VPS gratis
  con verificación de tarjeta.
- Pasos completos y seguridad: `resources/engineering/release/demo-gratis-antes-vps.md`.

## Relacionado

- [[tfm-triaje/validacion-motivos-catalogo|Validación de motivos + RIPS]]
- [[tfm-triaje/capitulos-tfm|Capítulos TFM]]
- [[tfm-triaje/evidencia-ingenieria|Evidencia de ingeniería]]
