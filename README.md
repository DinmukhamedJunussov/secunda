# Organization Directory API

Проект на FastAPI для хранения организаций, зданий и видов деятельности с поддержкой геопоиска и иерархий.

---

## Технологии

- Python 3.11
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Docker / Docker Compose

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone <url-репозитория>
cd secunda
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/Mac
# или
.venv\Scripts\activate  # для Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` в корневой директории проекта со следующими переменными:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/secunda
```

5. Запустите PostgreSQL (можно использовать Docker):
```bash
docker-compose up -d db
```

6. Примените миграции:
```bash
alembic upgrade head
```

7. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

Приложение будет доступно по адресу: http://localhost:8000
Документация API: http://localhost:8000/docs

### Запуск через Docker

1. Соберите и запустите контейнеры:
```bash
docker-compose up --build
```

Приложение будет доступно по адресу: http://localhost:8000
Документация API: http://localhost:8000/docs

## Структура проекта

```
secunda/
├── app/                    # Основной код приложения
├── alembic/               # Миграции базы данных
├── docker-compose.yml     # Конфигурация Docker Compose
├── Dockerfile            # Конфигурация Docker
├── requirements.txt      # Зависимости Python
└── alembic.ini          # Конфигурация Alembic
```

## Разработка

- Для создания новых миграций используйте:
```bash
alembic revision --autogenerate -m "описание изменений"
```

- Для применения миграций:
```bash
alembic upgrade head
```

- Для отката последней миграции:
```bash
alembic downgrade -1
```
