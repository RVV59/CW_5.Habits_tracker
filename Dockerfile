# C:/Users/Vlad/PycharmProjects/CW_5.Habits_tracker/Dockerfile

# Этап 1: Базовый образ с Python
# Используем официальный легковесный образ Python 3.11
FROM python:3.11-slim AS base

# Устанавливаем переменные окружения
# PYTHONUNBUFFERED: чтобы логи Python сразу выводились в консоль Docker
# PYTHONDONTWRITEBYTECODE: чтобы Python не создавал .pyc файлы
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Этап 2: Установка зависимостей
# Используем отдельный слой для зависимостей, чтобы Docker кэшировал его.
# Это ускорит последующие сборки, если зависимости не менялись.
FROM base as builder

# Устанавливаем Poetry
RUN pip install poetry

# Копируем только файлы с зависимостями
COPY poetry.lock pyproject.toml ./

# Устанавливаем зависимости проекта, игнорируя dev-зависимости (они не нужны в "боевом" образе)
# --no-root: не устанавливать сам проект как пакет, мы скопируем его позже
RUN poetry install --without dev --no-root

# Этап 3: Сборка финального образа
# Возвращаемся к базовому образу, чтобы финальный образ был меньше
FROM base

# Копируем виртуальное окружение с установленными зависимостями из слоя 'builder'
COPY --from=builder /root/.local /root/.local

# Устанавливаем путь к исполняемым файлам из виртуального окружения Poetry
ENV PATH=/root/.local/bin:$PATH

# Копируем весь код нашего приложения в рабочую директорию
COPY . .

# Открываем порт 8000, на котором будет работать gunicorn
EXPOSE 8000

# Команда, которая будет выполняться при запуске контейнера.
# Запускаем gunicorn, который будет слушать на порту 8000 и обслуживать наше приложение.
# config.wsgi - это путь к файлу wsgi.py в вашем проекте
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
