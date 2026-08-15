#!/bin/sh
set -e

# DB_PATH puede apuntar a un volumen (/app/data en docker compose)
if [ -n "$DB_PATH" ]; then
    mkdir -p "$(dirname "$DB_PATH")"
fi

echo "[triaje-ia] preparando base de datos y usuarios demo (idempotente)..."
python scripts/seed_demo.py

echo "[triaje-ia] verificación de plomería..."
python scripts/healthcheck.py

echo "[triaje-ia] arrancando Streamlit en 0.0.0.0:8501"
exec python -m streamlit run app/main.py --server.port 8501 --server.address 0.0.0.0
