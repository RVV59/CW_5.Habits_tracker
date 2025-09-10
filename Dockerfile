# C:/Users/Vlad/PycharmProjects/CW_5.Habits_tracker/Dockerfile

# Этап 1: Базовый образ с Python
FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Этап 2: Установка зависимостей
FROM base AS builder

RUN pip install poetry
COPY poetry.lock pyproject.toml ./

# Копируем весь код проекта (кроме того, что в .dockerignore)
COPY . .

# Устанавливаем зависимости, используя НОВЫЙ флаг для исключения dev-зависимостей
RUN poetry install --without dev

# Этап 3: Сборка финального образа
FROM base

# Устанавливаем netcat для ожидания БД
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# --- КЛЮЧЕВОЕ ИЗМЕНЕНИЕ ---
# Копируем виртуальное окружение в ту же директорию, что и в builder'е (/app/.venv)
COPY --from=builder /app/.venv /app/.venv

# Активируем виртуальное окружение, добавляя его в PATH
# Путь теперь более явный и находится внутри рабочей директории
ENV PATH="/app/.venv/bin:$PATH"
# -------------------------

# Копируем весь код нашего приложения еще раз, уже в финальный образ
COPY . .

EXPOSE 8000

# Команда для запуска. Теперь она точно найдет gunicorn из /app/.venv/bin/gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]