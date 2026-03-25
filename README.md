# SportNetwork

## Запуск через Docker Compose

Требования:
- Установлен Docker и Docker Compose.

Шаги:
1. Собрать и запустить сервисы:

```bash
docker compose up --build -d
```

2. Проверка сервиса:

```bash
curl http://localhost:8000/ping
```

3. Интерактивная документация:

перейдите на http://localhost:8000/docs
Ожидаемый ответ:


Остановка:

```bash
docker compose down
```
