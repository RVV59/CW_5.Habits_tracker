FROM python:3.11-slim AS base

# Устанавливаем переменные окружения
# PYTHONUNBUFFERED: чтобы логи Python сразу выводились в консоль Docker
# PYTHONDONTWRITEBYTECODE: чтобы Python не создавал .pyc файлы
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

FROM base as builder

RUN pip install poetry

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root
RUN #poetry install --without dev --no-root

FROM base

RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
# -------------------------
COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

ENV PYTHONPATH=/root/.local/lib/python3.11/site-packages
COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
