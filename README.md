# SportNetwork

Backend API для спортивной социальной сети.

## Требования

- Docker и Docker Compose
- OpenSSL (для генерации JWT ключей)

## Быстрый старт

### 1. Генерация JWT ключей

Для работы аутентификации необходимо сгенерировать пару RSA ключей:

```bash
# Создайте директорию для ключей (если не существует)
mkdir -p certs

# Сгенерируйте приватный ключ (2048 бит)
openssl genrsa -out certs/jwt-private.pem 2048

# Сгенерируйте публичный ключ
openssl rsa -in certs/jwt-private.pem -pubout -out certs/jwt-public.pem
```

### 2. Настройка переменных окружения

Скопируйте файл `.env.example` в `.env`:

```bash
cp .env.example .env
```

Заполните файл `.env` следующими переменными:

```bash
# БД PostgreSQL
DB_HOST=postgres
DB_PORT=5432
DB_USER=sport_network_user
DB_NAME=sport_network_db
DB_PASSWORD=ваш_надёжный_пароль
```

> **Примечание:** Минимально необходимые переменные для запуска — только `DB_*`. Остальные можно добавить по мере необходимости.

### 3. Запуск через Docker Compose

```bash
# Сборка и запуск всех сервисов
docker compose up --build -d

# Проверка доступности API
curl http://localhost:8000/ping
```

### 4. Проверка работы

- **API:** http://localhost:8000
- **Интерактивная документация (Swagger):** http://localhost:8000/docs
- **Альтернативная документация (ReDoc):** http://localhost:8000/redoc
- **RabbitMQ Management UI:** http://localhost:15672 (логин/пароль: `guest/guest`)
- **PostgreSQL:** localhost:5432
