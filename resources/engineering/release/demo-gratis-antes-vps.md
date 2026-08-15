# Demo gratuita ANTES del VPS — opciones validadas

**Fecha:** 2026-08-14 (actualizado) · Objetivo: navegar la demo públicamente
sin pagar, con HTTPS, mientras se tramita MIMIC-IV-ED y se decide el VPS.

## Respuesta corta

| Opción | ¿Sirve? | Seguridad | Recursos gratis | Por qué |
|---|---|---|---|---|
| **GitHub Pages** | ❌ NO | — | — | Solo contenido estático (HTML/CSS/JS). Sin Python ni WebSockets. |
| **Streamlit Community Cloud** | ✅ RECOMENDADO | HTTPS incluido + viewer allow-lists | ~1 GB RAM | Hecho para Streamlit, deploy desde este repo con un clic, se actualiza con cada `git push`. |
| **Hugging Face Spaces (CPU Basic)** | ✅ Alternativa robusta | HTTPS incluido | **2 vCPU · 16 GB RAM** | Soporta Streamlit y Docker; más RAM que Community Cloud; LFS nativo (modelos hasta 10 GB). |
| **GitHub Codespaces** | ⚠ Temporal | HTTPS en el forward público | horas gratis/mes | Demo puntual en vivo; se apaga al cerrar. |
| **Oracle Cloud Always Free** | ⚠ VPS completo gratis | Tú gestionas TLS (Caddy/certbot) | 4 vCPU ARM · 24 GB RAM · forever | Corre el Docker completo de producción; requiere tarjeta para verificar la cuenta (sin cobros en el free tier). |

## Recomendación

- **Hoy, para la demo:** Streamlit Community Cloud (menos pasos) o HF Spaces
  CPU Basic (más RAM si la inferencia se siente lenta). Ambos son seguros
  (HTTPS automático) y gratuitos sin tarjeta.
- **Cuando sea producción real:** VPS KVM 2 de Hostinger
  (ver `resources/engineering/release/despliegue-hostinger.md`).

## Opción 1 · Streamlit Community Cloud

1. Sube el repo a GitHub público (`git push`). ⚠ Nunca subir `datasets/`.
2. Entra a **share.streamlit.io** → "Deploy an app" (login con GitHub).
3. Repositorio `erick880709/Kit-IA` · Rama `main` · **Main file path:** `triaje-ia/app/main.py`.
4. Secrets de la app:
   ```
   APP_SECRET_KEY = <clave aleatoria de 32 bytes hex>
   MODELS_DIR = triaje-ia/artifacts/models
   DB_PATH = triaje.db
   ```
5. "Deploy" → URL pública `https://<app>.streamlit.app` (login demo:
   `medico@hospital.gov.co` / `Demo123!` — el seed corre solo).

## Opción 2 · Hugging Face Spaces (CPU Basic, 16 GB gratis)

1. Crea el Space en **huggingface.co/new-space** → SDK **Streamlit** (o Docker).
2. Con SDK Streamlit: sube el contenido de `triaje-ia/` a la raíz del Space
   (incluye `app.py` shim ya preparado, `requirements.txt`, `.streamlit/`,
   `app/`, `ml/src/`, `scripts/`, `assets/`, `artifacts/models/`).
   - Con Docker: sube el `Dockerfile` de `triaje-ia/` y construye el Space como Docker.
3. Secrets del Space: `APP_SECRET_KEY`, `MODELS_DIR=artifacts/models`.
4. URL pública: `https://<usuario>-<espacio>.hf.space`.

## Seguridad (aplica a ambas)

- HTTPS por defecto en las dos plataformas (certificados gestionados).
- La app es **pública**: es demo académica con datos SINTÉTICOS — nunca subir
  datos reales ni la carpeta `datasets/`.
- Usar siempre `APP_SECRET_KEY` propia (rotar de la demo).
- Community Cloud permite además restringir viewers con allow-lists.

## Después de la demo

- Cuando llegue MIMIC-IV-ED, se reentrena en local y se re-despliega.
- Para producción: VPS KVM 2 de Hostinger o el Always Free de Oracle (Docker completo).
