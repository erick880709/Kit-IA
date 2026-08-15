# Guía de despliegue — Hostinger VPS (TriajeIA)

**Fecha:** 2026-08-14 · Imagen Docker disponible: `triaje-ia:demo` (2,62 GB)

## 1. Producto recomendado: VPS KVM 2

| Plan | vCPU | RAM | NVMe | Ancho de banda | Precio promo (2 años) | Renovación |
|---|---|---|---|---|---|---|
| KVM 1 | 1 | 4 GB | 50 GB | 4 TB | $6.49/mes | $11.99/mes |
| **KVM 2 (recomendado)** | **2** | **8 GB** | **100 GB** | **8 TB** | **$8.79/mes** | $14.99/mes |
| KVM 4 | 4 | 16 GB | 200 GB | 16 TB | $12.99/mes | $28.99/mes |
| KVM 8 | 8 | 32 GB | 400 GB | 32 TB | $25.99/mes | $49.99/mes |

**Por qué KVM 2:**
- La imagen pesa 2,62 GB y la construcción en el servidor (`pip install` de
  xgboost/shap) pica ~2-3 GB de RAM — KVM 1 (4 GB) queda justo; KVM 2 da margen.
- 100 GB NVMe cubren imagen + volúmenes de BD/logs + backups.
- Incluye: root completo, **Docker de un clic**, gestor de Docker Compose,
  firewall gestionado, DDoS, backups semanales, dominio gratis 1 año,
  garantía de 30 días.
- **Descartar:** el hosting compartido/Cloud Hosting de Hostinger NO admite
  Docker ni puertos propios — no sirve para esta app.
- Si solo vas a desplegar la imagen ya construida (subiéndola a un registry),
  KVM 1 alcanza; si construirás en el servidor, KVM 2.

## 2. Qué adquirir (lista de compra)

1. **VPS KVM 2** (plan de 24 meses para el precio promo; renovación $14.99/mes).
2. Plantilla **Ubuntu 24.04** con la app **Docker** (despliegue de un clic).
3. **Dominio** (incluido gratis el primer año) o usar la IP del VPS.
4. Ubicación del datacenter: **São Paulo (Sudamérica)** para mejor latencia desde Colombia.

## 3. Pasos de despliegue

```bash
# 1. Clonar el repo en el VPS
git clone https://github.com/erick880709/Kit-IA.git
cd Kit-IA/triaje-ia

# 2. Clave de sesión propia (NUNCA la de la demo)
export APP_SECRET_KEY=$(openssl rand -hex 32)

# 3. Construir y arrancar (Docker incluido en la plantilla)
docker compose up -d --build

# 4. Abrir el puerto 8501 en el firewall de hPanel
```

```yaml
# Ajustar docker-compose.yml antes del arranque:
services:
  triaje-ia:
    build: .
    ports:
      - "127.0.0.1:8501:8501"   # solo local; el TLS lo termina el proxy
    environment:
      APP_SECRET_KEY: ${APP_SECRET_KEY}
      DB_PATH: /app/data/triaje.db
```

5. **TLS:** instalar Caddy o nginx + certbot como reverse proxy:
   `https://triaje.dominio → http://127.0.0.1:8501`.
6. **Verificar:** `docker ps` (estado healthy), login demo, HEALTHCHECK en `/_stcore/health`.
7. **Backups:** los incluidos semanales del VPS + volúmenes `triaje_data` y `triaje_logs`.

## 4. Costo estimado

- Año 1-2: **~$8.79/mes** (KVM 2, plan 2 años) ≈ **$211 por 24 meses**.
- Sin costos extra obligatorios (dominio gratis 1 año, backups incluidos).
- Garantía de reembolso de 30 días.
