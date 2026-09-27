FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN useradd --create-home appuser

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=appuser:appuser assets ./assets
COPY --chown=appuser:appuser gbs ./gbs
COPY --chown=appuser:appuser montecarlo ./montecarlo
COPY --chown=appuser:appuser ui ./ui
COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE 8050

HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8050/healthz')"

# A single worker keeps memory within the default 256 MiB allocation; threads serve concurrent users.
CMD ["gunicorn", "app:server", "--bind", "0.0.0.0:8050", "--workers", "1", "--threads", "4", "--timeout", "120"]
