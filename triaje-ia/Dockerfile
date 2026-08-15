# TriajeIA — demo de triaje multimodal con IA (TFM UNIR)
# Construcción:  docker build -t triaje-ia:demo .
# Ejecución:     docker run -p 8501:8501 triaje-ia:demo
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

WORKDIR /app

# curl: solo para el HEALTHCHECK del contenedor
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Dependencias Python (rueda completa: streamlit, sklearn, xgboost, shap)
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Código de la aplicación (solo lo necesario en runtime — sin tests ni datos)
COPY app ./app
COPY ml/src ./ml/src
COPY scripts ./scripts
COPY .streamlit ./.streamlit
COPY assets ./assets
COPY artifacts/models ./artifacts/models
COPY artifacts/shap ./artifacts/shap
COPY .env.example ./.env.example

# .env local de la demo (en un servidor real: montar secretos desde fuera)
RUN test -f .env || cp .env.example .env

# Usuario sin privilegios
RUN useradd --create-home --shell /usr/sbin/nologin triaje \
    && mkdir -p /app/data /app/logs \
    && chown -R triaje:triaje /app
USER triaje

COPY --chown=triaje:triaje docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=90s --retries=3 \
    CMD curl -fsS http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["docker-entrypoint.sh"]
