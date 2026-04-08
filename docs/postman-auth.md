# Авторизация — Postman Guide

## 1. Регистрация нового пользователя

**Метод:** `POST`  
**URL:** `http://localhost:8000/users/register`

### Body → raw → JSON

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "SecurePass123",
  "date_of_birth": "1990-01-01",
  "gender": "male"
}
```

> `gender` принимает: `man`, `women`

### Response (200)

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": false
}
```

> После регистрации в БД создаётся пользователь с `is_active=false` и уникальным `token`.  
> В фоне отправляется задача `send_verify_email` на SMTP сервер.

### curl

```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123",
    "date_of_birth": "1990-01-01",
    "gender": "male"
  }'
```

---

## 2. Верификация почты

### 2.1 Получить токен из БД

```bash
docker compose exec postgres psql -U kirill -d sport_network \
  -c "SELECT token FROM users WHERE email = 'test@example.com';"
```

Скопируй UUID из колонки `token`.

### 2.2 Перейти по ссылке верификации

**Метод:** `GET`  
**URL:** `http://localhost:8000/users/verify-email?token=<твой-uuid>`

Открой в браузере или выполни в Postman → вкладка **Params** → добавь `token`.

### Результат

- **Успех** → редирект `307` на `/verify-email/success`
- **Ошибка** → `400 Bad Request`:
  - `"Invalid or expired verification token"` — токен не найден
  - `"Email already verified"` — email уже подтверждён

### curl

```bash
curl "http://localhost:8000/users/verify-email?token=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### Проверка в БД

```bash
docker compose exec postgres psql -U kirill -d sport_network \
  -c "SELECT id, username, email, is_active FROM users WHERE email = 'test@example.com';"
```

`is_active` должен быть `t`.

---

## 3. Вход в аккаунт (Login)

**Метод:** `POST`  
**URL:** `http://localhost:8000/users/login`

### Body → raw → JSON

По username:

```json
{
  "identifier": "testuser",
  "password": "SecurePass123"
}
```

По email:

```json
{
  "identifier": "test@example.com",
  "password": "SecurePass123"
}
```

### Response (200)

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true,
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Set-Cookie заголовки

В ответе приходят два httpOnly cookie:

| Cookie | HttpOnly | Secure | SameSite | Max-Age |
|--------|----------|--------|----------|---------|
| `access_token` | ✓ | ✓ | lax | 3600s (1 час) |
| `refresh_token` | ✓ | ✓ | lax | 604800s (7 дней) |

> В Postman: вкладка **Cookies** → если включён `Automatically follow cookies`, они сохранятся автоматически.

### Уведомление о входе

В фоне отправляется задача `send_login_notification` на email пользователя с информацией:
- IP-адрес (из `X-Forwarded-For` или `request.client.host`)
- Устройство (Desktop / Mobile / Tablet — парсится из User-Agent)
- Браузер (Chrome / Firefox / Safari / Edge / Unknown)

### curl

```bash
curl -v -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"testuser","password":"SecurePass123"}'
```

> Обрати внимание на `Set-Cookie` в заголовках ответа.

---

## 4. Получить информацию о текущем пользователе

**Метод:** `GET`  
**URL:** `http://localhost:8000/users/me`

### Вариант A — Cookie (автоматически)

Если Postman сохранил cookies из login-запроса — просто отправь GET.

### Вариант B — Bearer Token

Вкладка **Authorization** → Type: `Bearer Token` → вставь `access_token` из ответа login.

Или вручную в **Headers**:

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Response (200)

```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "is_active": true
}
```

### Response (401) — без токена

```json
{
  "detail": "Not authenticated"
}
```

### Response (401) — токен истёк

```json
{
  "detail": "Token has expired"
}
```

### curl

```bash
curl http://localhost:8000/users/me \
  -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Быстрый сценарий: полный цикл

```bash
# 1. Регистрация
RESPONSE=$(curl -s -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"SecurePass123","date_of_birth":"1990-01-01","gender":"male"}')
echo "$RESPONSE"

# 2. Получить токен верификации
TOKEN=$(docker compose exec -T postgres psql -U kirill -d sport_network -t -A \
  -c "SELECT token FROM users WHERE email = 'test@example.com' AND token IS NOT NULL LIMIT 1;")

# 3. Верификация
curl "http://localhost:8000/users/verify-email?token=$TOKEN"

# 4. Логин (сохраняем cookie в файл)
curl -c /tmp/cookies.txt -s -X POST http://localhost:8000/users/login \
  -H "Content-Type: application/json" \
  -d '{"identifier":"testuser","password":"SecurePass123"}' -o /dev/null

# 5. Получить me (используем cookie)
curl -b /tmp/cookies.txt http://localhost:8000/users/me
```

---

## Ошибки

| Код | Причина |
|-----|---------|
| `400` | Email или username уже занят |
| `400` | Пароль < 8 символов |
| `400` | Неверный токен верификации |
| `400` | Email уже верифицирован |
| `401` | Неверные учётные данные (логин/пароль) |
| `401` | Токен отсутствует |
| `401` | Токен истёк |
| `401` | Пользователь не найден (удалён после выдачи токена) |
