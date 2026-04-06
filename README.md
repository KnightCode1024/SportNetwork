# SportNetwork

- Backend API приложения для поиска спортивных мероприятий.
- [Frontend](https://github.com/Ox000O00/SportNetwork)

## Требования
- Docker и Docker Compose
- OpenSSL (для генерации JWT ключей)

## Запуск

### 1. Генерация JWT ключей
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


## Архитектура
Архитектура приложение базируется на прицыпах чистой архитектуры. 

- `ioc` - di фрэфмвок. Принцып инверсии зависимости.
- `config` - Настройки приложения
- `application`
- `controllers` - Слой представления
  - `api` - Эндпоинты/Ручки
  - `schemas` - Схемы валидации данных в слое представленияъ
- `domain` - Доменные модели.
- `infrastructure` - Инфраструктурный слой. Работа с данными
