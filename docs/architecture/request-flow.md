# Порядок выполнения запросов

## На примере регистрации пользователя

```
Client (браузер)
    │
    │  POST /users/register
    │  {username, email, password, age, gender}
    ▼
┌────────────────────────────────────────────────────┐
│  1. CONTROLLER (users_controller.py)               │ 
│  • Принимает HTTP-запрос                           │      
│  • Валидирует входные данные через Pydantic Schema │  
│        (RegisterRequest)                           │ 
│  • Создаёт Input DTO из запроса                    │ 
│  • Вызывает interactor                             │ 
└──────────────┬─────────────────────────────────────┘
               │ input_data = RegisterUserInput(...)
               ▼
┌───────────────────────────────────────────────┐
│  2. IOC CONTAINER (Dishka)                    │
│  • Разрешает зависимости:                     │
│    - UnitOfWork (создаёт DB session)          │
│    - UserGateway (получает session из UoW)    │
│    - ProfileGateway (получает session из UoW) │
│    - PasswordService (singleton)              │
│  • Инжектирует их в RegisterUserInteractor    │
└──────────────┬────────────────────────────────┘
               │ interactor с инъекциями
               ▼
┌─────────────────────────────────────────────┐
│  3. INTERACTOR (RegisterUserInteractor)     │ 
│  • Управляет транзакцией через UoW          │ 
│  • Содержит бизнес-логику регистрации       │ 
│                                             │
│  async with self.uow:  ← начало транзакции  │
│      1. Проверка email на уникальность      │  
│      2. Проверка username на уникальность   │
│      3. Хеширование пароля                  │
│      4. Создание User domain model          │
│      5. Сохранение User через gateway       │
│      6. Создание Profile domain model       │
│      7. Сохранение Profile через gateway    │
│      ← auto-commit при успехе               │
│      ← rollback при ошибке                  │
└──┬──────────────────────┬───────────────────┘
   │                      │
   ▼                      ▼
┌─────────────┐  ┌─────────────────────────┐
│  GATEWAY    │  │       UNIT OF WORK      │
│(User,       │  │                         │
│ Profile)    │  │ • Начинает транзакцию   │
│             │  │ • Предоставляет session │
│ Gateway     │  │ • Коммитит/rollback     │
│ реализует   │  │ • Закрывает session     │
│ интерфейс   │  └─────────────────────────┘
│ из          │
│ application/│
└────┬────────┘
     │ SQL запросы
     ▼
┌─────────────────────────────────┐
│  4. DATABASE (PostgreSQL)       │
│  • Выполняются SQL операции     │
│  • Возвращаются результаты      │
└──────────────┬──────────────────┘
               │ domain model
               ▼
┌─────────────────────────────────┐
│  5. INTERACTOR → DTO            │
│  • Преобразует User domain model│
│    в RegisterUserDTO            │
│  • Возвращает DTO в controller  │
└──────────────┬──────────────────┘
               │ RegisterUserDTO
               ▼
┌─────────────────────────────────────────────┐
│  6. CONTROLLER → RESPONSE                   │
│  • Получает DTO от interactor               │
│  • Создаёт HTTP Response (RegisterResponse) │
│  • FastAPI сериализует в JSON               │
└──────────────┬──────────────────────────────┘
               │ HTTP 200 OK
               │ {id, username, email, is_active}
               ▼
         Client получает ответ
```

## Общая схема для любого запроса

1. `HTTP Request` → FastAPI Router
2. `Pydantic Validation` → входные данные
3. `DI Resolution` → Dishka создаёт/получает зависимости
4. `Interactor Execution` → бизнес-логика с транзакцией
5. `DTO Return` → данные возвращаются через слои
6. `HTTP Response` → сериализация в JSON
