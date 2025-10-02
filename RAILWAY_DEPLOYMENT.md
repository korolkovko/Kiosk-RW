# KIOSK Backend - Railway Deployment Guide

Backend для киоска самообслуживания, готовый к развертыванию на Railway.

## Технологический стек

- **FastAPI** - веб-фреймворк
- **PostgreSQL** - основная база данных
- **Redis** - кеширование и сессии
- **SQLAlchemy** - ORM
- **Alembic** - миграции базы данных

## Развертывание на Railway

### 1. Создание проекта

1. Войдите в [Railway](https://railway.app)
2. Создайте новый проект
3. Подключите этот GitHub репозиторий

### 2. Добавление сервисов

Добавьте следующие сервисы в ваш проект:

#### PostgreSQL
```
+ New → Database → PostgreSQL
```

#### Redis
```
+ New → Database → Redis
```

### 3. Настройка переменных окружения

В настройках вашего веб-сервиса добавьте следующие переменные:

```bash
# Application Settings
PROJECT_NAME=KIOSK Application
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this

# Database (автоматически из Railway PostgreSQL)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (автоматически из Railway Redis)
REDIS_URL=${{Redis.REDIS_URL}}

# JWT Settings
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1800

# CORS Settings
ALLOWED_ORIGINS=["https://your-frontend-domain.com"]

# External Integrations (опционально)
POS_API_URL=
POS_API_KEY=
PAYMENT_API_URL=
PAYMENT_API_KEY=
```

### 4. Автоматический деплой

Railway автоматически:
- Обнаружит Python проект через `requirements.txt`
- Установит зависимости
- Запустит приложение согласно `Procfile` или `railway.toml`

### 5. Проверка работоспособности

После деплоя проверьте следующие эндпоинты:

```
GET https://your-app.railway.app/
GET https://your-app.railway.app/health
GET https://your-app.railway.app/api/v1/openapi.json
```

## Структура проекта

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── auth/         # Аутентификация
│   │   ├── database/     # Модели БД
│   │   ├── logic/        # Бизнес-логика
│   │   ├── models/       # Pydantic модели
│   │   ├── services/     # Сервисы
│   │   ├── config.py     # Конфигурация
│   │   └── main.py       # Точка входа
│   └── alembic/          # Миграции БД
├── Procfile              # Railway команда запуска
├── railway.toml          # Railway конфигурация
└── requirements.txt      # Python зависимости
```

## База данных

### Модели данных

Основные таблицы:
- `users` - пользователи системы (админы, персонал)
- `roles` - роли и права доступа
- `known_customers` - зарегистрированные клиенты
- `sessions` - активные сессии
- `items_live` - активное меню
- `items_live_available` - остатки товаров
- `orders` - заказы
- `payments` - платежи
- `devices` - устройства (киоски, терминалы)
- `branches` - филиалы

### Миграции

Миграции применяются автоматически при старте приложения через SQLAlchemy:

```python
Base.metadata.create_all(bind=engine)
```

Для создания новых миграций с Alembic:

```bash
cd backend
alembic revision --autogenerate -m "описание изменений"
```

## API Документация

После деплоя автоматически доступна документация:

- **Swagger UI**: `https://your-app.railway.app/api/v1/docs`
- **ReDoc**: `https://your-app.railway.app/api/v1/redoc`
- **OpenAPI JSON**: `https://your-app.railway.app/api/v1/openapi.json`

## Основные эндпоинты

### Аутентификация
- `POST /api/v1/auth/login` - вход
- `POST /api/v1/auth/refresh` - обновление токена
- `POST /api/v1/auth/logout` - выход

### Пользователи
- `GET /api/v1/users` - список пользователей
- `POST /api/v1/users` - создание пользователя
- `GET /api/v1/users/{user_id}` - информация о пользователе

### Меню
- `GET /api/v1/items` - получить все товары
- `POST /api/v1/items` - добавить товар
- `PATCH /api/v1/items/{item_id}` - обновить товар
- `POST /api/v1/items/{item_id}/stock` - пополнить остатки

## Важные замечания

### Файловое хранилище

⚠️ **Функционал загрузки файлов отключен** для Railway, так как используется ephemeral filesystem.

Для хранения файлов (изображения товаров, документы) рекомендуется:
- AWS S3
- Cloudinary
- Railway Volumes (для постоянного хранения)

### Логирование

Railway автоматически собирает логи из stdout/stderr. Настройка `LOG_FILE_PATH` игнорируется.

### Переменные окружения

Все чувствительные данные должны быть в переменных окружения Railway, никогда не коммитьте `.env` файл!

## Безопасность

Обязательно измените:
- `SECRET_KEY` - для шифрования сессий
- `JWT_SECRET_KEY` - для JWT токенов
- Используйте сложные, случайные строки (минимум 32 символа)

Генерация случайных ключей:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Мониторинг

Railway предоставляет:
- Логи в реальном времени
- Метрики использования (CPU, RAM, Network)
- Автоматические перезапуски при сбоях

## Разработка локально

```bash
# Установка зависимостей
pip install -r requirements.txt

# Создание .env файла (скопируйте из backend/.env.example)
cp backend/.env.example backend/.env

# Запуск PostgreSQL и Redis через Docker
docker-compose up -d

# Запуск приложения
cd backend
uvicorn app.main:app --reload
```

## Поддержка

При возникновении проблем проверьте:
1. Логи в Railway Dashboard
2. Переменные окружения
3. Подключение к PostgreSQL и Redis
4. Правильность DATABASE_URL формата: `postgresql://user:password@host:port/database`

## Лицензия

Проприетарное ПО. Все права защищены.
