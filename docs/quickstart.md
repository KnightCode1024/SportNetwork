# Быстрый старт

## Требования

- Docker и Docker Compose
- OpenSSL (для генерации JWT ключей)

## 1. Генерация JWT ключей

Для работы аутентификации необходимо сгенерировать пару RSA ключей:

```bash
# Создайте директорию для ключей (если не существует)
mkdir -p certs

# Сгенерируйте приватный ключ (2048 бит)
openssl genrsa -out certs/jwt-private.pem 2048

# Сгенерируйте публичный ключ
openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
```

## 2. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env`:

```bash
cp .env.example .env
```

Заполните файл `.env` следующими переменными:

```bash
DB_HOST=postgres_sport_network
DB_PORT=5432
DB_USER=sport_network_user
DB_NAME=sport_network_db
DB_PASSWORD=12345678

APP_NAME=sport-network
APP_MODE=dev
APP_HOST=0.0.0.0
APP_PORT=8001
APP_SECRET_KEY=secret_key

S3_ENDPOINT=http://minio:9000
S3_PUBLIC_KEY=admin
S3_ACCESS_KEY=admin
S3_SECRET_KEY=secret-key
S3_BUCKET_NAME=sport-network
S3_REGION=us-east-1

EMAIL_PASSWORD=bimzacfkfuspdftj
EMAIL_HOST=smtp.yandex.ru
EMAIL_PORT=465
EMAIL_USER=n17k17@yandex.ru
EMAIL_USE_SSL=1

REDIS_PORT=6379
REDIS_HOST=redis_sport_network

RABBITMQ_HOST=rabbitmq_sport_network
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest

FRONTEND_URL=http://127.0.0.1:3000

GOOGLE_CLIENT_ID=str
GOOGLE_CLIENT_SECRET=str
GOOGLE_REDIRECT_URL=HttpUrl
```

## 3. Запуск через Docker Compose

```bash
# Сборка и запуск всех сервисов
docker compose up --build -d

# Проверка доступности API
curl http://localhost:8000/ping
```

## 4. Проверка работы

- `API` -  `http://localhost:8001/api/v1/`
- `API документация` - `http://localhost:8000/docs`
