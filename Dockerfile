FROM python:3.11-slim

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY src /app/src

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir .

ENV MEMORY_DB_PATH=/app/data/memory.db
EXPOSE 8000
CMD ["uvicorn", "memory_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
