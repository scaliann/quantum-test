# Posts Management System

Система управления постами с аутентификацией пользователей, состоящая из трех основных сервисов.

## Установка и запуск


### Настройка окружения

1. Создайте файл `.env` в корневой директории:
```env
BOT_TOKEN=token
DATABASE_URL=postgresql+asyncpg://postgres:postgres@db:5432/posts_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=posts_db
API_URL=http://api:8000
```

### Запуск проекта

Сборка и запуск контейнеров:
```bash
docker-compose up -d
```

### Доступ к сервисам

- Frontend: http://localhost
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Telegram bot: @quantumm_test_bot

### Как управлять постами

- Зайдите на http://localhost
- Введите тестовые email и пароль и нажмите "Зарегистрироваться"
- Готово! Теперь вы можете создавать, изменять и удалять посты
- Зайдите в Telegram bot @quantumm_test_bot
- Чтобы получить весь список постов, воспользуйтесь командой /post

## Структура проекта

```
quantum_tesе_auth/
├── api_service/         # FastAPI бэкенд сервис
│   ├── src/
│   │   ├── posts/      # Модуль для работы с постами
│   │   ├── users/      # Модуль аутентификации и пользователей
│   │   ├── config.py   # Конфигурация приложения
│   │   ├── database.py # Настройки базы данных
│   │   └── main.py     # Точка входа FastAPI приложения
│   ├── Dockerfile
│   └── requirements.txt
├── frontend_service/    # Веб-интерфейс
│   ├── index.html      # Главная страница
│   ├── nginx.conf      # Конфигурация Nginx
│   └── Dockerfile
├── bot_service/        # Телеграм бот сервис для чтения постов
├── docker-compose.yml  # docker-compose для управления всеми сервисами
└── .env/           # Настройки всего проекта
```

## Сервисы

### API Service
- RESTful API на FastAPI
- Аутентификация пользователей с JWT токенами
- CRUD операции для постов
- PostgreSQL база данных
- Асинхронное взаимодействие с БД через SQLAlchemy

### Frontend Service
- Single Page Application (SPA)
- Чистый HTML/CSS/JavaScript
- Nginx для раздачи статики
- Интерактивный интерфейс для работы с постами
- Аутентификация пользователей

### Bot Service
- Telegram бот для взаимодействия с системой
- Интеграция с API сервисом
- Aiogram в качестве библиотеки

## Технологический стек

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy (async)
- Alembic
- PostgreSQL
- JWT для аутентификации
- Pydantic для валидации данных

### Frontend
- HTML5
- CSS3
- JavaScript
- Nginx

### Infrastructure
- Docker
- Docker Compose
- Nginx


## API Endpoints

### Пользователи
- POST /users/register - Регистрация нового пользователя
- POST /users/login - Аутентификация пользователя
- POST /users/logout - Выход из системы

### Посты
- GET /posts - Получение списка всех постов
- GET /posts/{id} - Получение конкретного поста
- POST /posts - Создание нового поста
- PUT /posts/{id} - Обновление поста
- DELETE /posts/{id} - Удаление поста
