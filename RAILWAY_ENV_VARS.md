# Railway Environment Variables

Скопируйте эти переменные в Railway Dashboard → Settings → Variables

## Обязательные переменные

```bash
# Application Settings
PROJECT_NAME=KIOSK Application
API_V1_STR=/api/v1
ENVIRONMENT=production
DEBUG=false

# Security Keys (ВАЖНО: сгенерируйте новые для production!)
SECRET_KEY=WBDbVogisGwKGcydJSiiE6kQMWWtFPfuLbK6SEfxqo4
JWT_SECRET_KEY=iGW4jwyqaTK-cTAIJL-PtE2dF3FQWABeRKi--8NguCo

# Database (автоматически подставится из Railway PostgreSQL)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Redis (автоматически подставится из Railway Redis)
REDIS_URL=${{Redis.REDIS_URL}}

# JWT Settings for Admin/Staff
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Kiosk Authentication - Extended JWT for self-service kiosks
KIOSK_JWT_SECRET_KEY=k1i2o3s4k5_6s7e8c9r0e1t2_3k4e5y6_7f8o9r0_1l2o3n4g5_6l7i8v9e0d1_2t3o4k5e6n7s8
KIOSK_JWT_ALGORITHM=HS256
KIOSK_ACCESS_TOKEN_EXPIRE_DAYS=30
KIOSK_REFRESH_TOKEN_EXPIRE_DAYS=90
KIOSK_JWT_KEY_ID=kiosk-key-2025-v1

# CORS (добавьте ваш Railway домен!)
ALLOWED_ORIGINS=["https://your-app.railway.app","https://your-frontend.railway.app"]

# Logging
LOG_LEVEL=INFO
```

## Опциональные переменные (можно не добавлять)

```bash
# Server settings (Railway автоматически установит PORT)
# HOST=0.0.0.0
# PORT=$PORT

# File uploads (отключены на Railway)
# MAX_FILE_SIZE=10485760
# UPLOAD_PATH=./uploads

# Logging paths (Railway использует stdout/stderr)
# LOG_FILE_PATH=./logs/app.log

# External integrations (добавьте когда будут готовы)
POS_API_URL=
POS_API_KEY=
PAYMENT_API_URL=
PAYMENT_API_KEY=
```

## Важно! Безопасность

### 1. Сгенерируйте новые SECRET_KEY для production:

Выполните локально и скопируйте результаты:

```bash
# SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# KIOSK_JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

### 2. Обновите ALLOWED_ORIGINS

После деплоя добавьте реальный Railway домен:

```bash
ALLOWED_ORIGINS=["https://kiosk-rw-production.railway.app"]
```

## Пошаговая инструкция

1. **Зайдите в Railway Dashboard**
2. **Откройте ваш backend сервис**
3. **Перейдите в Variables**
4. **Добавьте все переменные из раздела "Обязательные переменные"**
5. **Сгенерируйте новые ключи безопасности** (см. команды выше)
6. **Замените тестовые ключи на production**
7. **Сохраните изменения**

Railway автоматически перезапустит сервис с новыми переменными.

## Проверка после деплоя

После успешного деплоя проверьте:

```bash
# Health check
curl https://your-app.railway.app/health

# API docs
https://your-app.railway.app/api/v1/docs
```

## Troubleshooting

Если приложение не запускается, проверьте логи на ошибки:

- ✅ `DATABASE_URL` правильно ссылается на PostgreSQL сервис
- ✅ `REDIS_URL` правильно ссылается на Redis сервис
- ✅ Все обязательные переменные заполнены
- ✅ Нет опечаток в названиях переменных
