Приложение для Благотворительного фонда поддержки котиков QRKot

созданно с использованием:
Python
FastAPI
FastAPI-Users
SQLAlchemy
Alembic
Pydantic

как использовать проект:
 1) Склонировать репозиторий: git clone
 2) Создать и активировать виртуальное окружение:
    python -m venv venv
    source venv/Scripts/activate  для win
    source venv/bin/activate      для lin
 3) Установить зависимости: pip install -r requirements.txt
 4) Создать .env файл по примеру .env.example
 5) Применит миграции: alembic upgrade head
 6) Запустить сервер: uvicorn app.main:app --reload