FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN useradd --create-home appuser

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY --chown=appuser:appuser .streamlit ./.streamlit
COPY --chown=appuser:appuser montecarlo ./montecarlo
COPY --chown=appuser:appuser app.py .

USER appuser

EXPOSE 8501

HEALTHCHECK CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')"

CMD ["streamlit", "run", "app.py"]
