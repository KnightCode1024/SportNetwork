# SportNetwork — Project Context for AI Agents

## Project Structure

```
src/sport_network_api/
├── config/           # Pydantic-settings configs (email, frontend, auth_jwt, etc.)
├── domain/           # Domain models (dataclass, business logic methods)
├── application/      # Application layer
│   ├── dto/          # Data transfer objects (dataclass)
│   ├── interactors/  # Use cases (business logic)
│   └── interfaces/   # Protocols (gateways, services, UoW)
├── infrastructure/   # Infrastructure layer
│   ├── gateways/     # Repository implementations
│   ├── migrations/   # Alembic migrations
│   ├── services/     # External services (JWT, password, email)
│   ├── tasks/        # TaskIQ async tasks
│   ├── models/       # SQLAlchemy models
│   └── taskiq_broker.py
├── controllers/      # Presentation layer (FastAPI routers)
│   ├── api/v1/       # Endpoints
│   └── schemas/      # Pydantic request/response models
└── ioc/              # Dependency Injection (dishka)
    └── providers/    # Auth, Config, Database, Gateways, Interactors, Services, UoW
```

## Architecture: Clean Architecture + DI

### Layer Flow
```
Request → Controller → Interactor → Gateway → DB
                    ↕              ↕
                DTO (dataclass)  UoW
```

### Key Conventions

#### Domain Models (`domain/`)
- Plain `@dataclass`, NOT Pydantic
- Contain business logic methods (e.g. `User.verify_password()`, `User.activate()`)
- `id: int | None` — None before creation, set by DB after insert

#### DTOs (`application/dto/`)
- Also `@dataclass`, NOT Pydantic
- Used for data transfer between interactors and controllers
- `*Input` — input data, `*DTO` — output data

#### Controllers (`controllers/`)
- Pydantic models for request/response schemas (`controllers/schemas/`)
- Inject dependencies via `FromDishka[...]`
- Return Pydantic models directly (FastAPI serializes to JSON)
- Set cookies on `Response` parameter (FastAPI attaches them to the serialized model)

#### Interactors (`application/interactors/`)
- Contain all business logic
- Take DTOs as input, return DTOs as output
- Use UoW context manager: `async with self.uow:` — auto-commits on success
- Tasks (taskiq) called OUTSIDE the `async with self.uow:` block (after commit)
- Device parsing, identifier resolution — belongs here, NOT in controllers

#### Unit of Work (`infrastructure/unit_of_work.py`)
- `async with uow:` — creates session, auto-commits on `__aexit__` (if no exception)
- On exception — auto-rollback
- Has explicit `commit()` and `rollback()` methods

#### Providers (`ioc/providers/`)
- `AuthProvider` — decodes JWT from cookie or Authorization header, returns `UserResponse`
- `FastapiProvider()` — already registered, allows injecting `Request` into providers
- `ServiceProvider` — Scope.APP (singletons: PasswordService, JwtService)
- `GatewayProvider`, `InteractorProvider` — Scope.REQUEST

## Authentication Flow

### JWT
- RS256 (asymmetric): private key for encode, public key for decode
- `access_token` — expires in `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 60)
- `refresh_token` — expires in `REFRESH_TOKEN_EXPIRE_DAYS` (default: 7)
- Payload: `{"sub": user_id, "email": user_email}`
- Keys in `certs/jwt-private.pem` and `certs/jwt-public.pem`

### Login
1. Controller extracts `identifier` (username OR email) + `password`
2. Interactor determines type: `"@" in identifier` → email, else → username
3. Verifies password via `User.verify_password()` (bcrypt)
4. Creates access + refresh tokens
5. Sends `send_login_notification` task (IP, device, browser from User-Agent)
6. Controller sets httpOnly cookies for both tokens

### Registration
1. Creates user with `is_active=False`, `token=uuid4()`
2. Sends `send_verify_email` task (link: `/verify-email?token=<token>`)
3. User clicks link → `VerifyEmailInteractor` finds by token, calls `user.activate()`

## TaskIQ Tasks

- `send_verify_email` — verification email with activation link
- `send_login_notification` — security notification about new login
- Tasks registered in `infrastructure/tasks/__init__.py`
- Broker imports tasks module to auto-discover them
- For dev: `InMemoryBroker`, for prod: `AioPikaBroker` (RabbitMQ)

## Alembic Migrations

- Async: uses `asyncpg` dialect
- Adding NOT NULL column to table with data requires 2-step migration:
  1. Add column as `nullable=True` + generate values for existing rows
  2. `alter_column` to `nullable=False`
- Use named constraints: `op.create_unique_constraint('name', 'table', ['col'])`

## Docker

```yaml
# compose.yml
services:
  postgres: 5432
  rabbitmq: 5672 / 15672 (management)
  backend: 8000 (runs: alembic upgrade head && uvicorn --reload)
```

- Working dir in container: `/backend`
- `PYTHONPATH=src`
- Volumes: `.:/backend`, `.env:/backend/.env:ro`, `certs:/backend/certs:ro`

## Config

- All configs use `pydantic-settings` with `ENV_FILE` (`.env`)
- `EmailConfig` — prefix `EMAIL_`
- `FrontendConfig` — prefix `_FRONTEND_`
- `AuthJWTConfig` — prefix from env vars (keys path, algorithm, expire times)
- `APPConfig` — prefix `APP_` (NAME, MODE, HOST, PORT, SECRET_KEY)

## Common Gotchas

1. **`default=uuid4` NOT `default=uuid4()`** — function reference, not call
2. **Tasks after commit** — `async with self.uow:` exits → then `.kiq(...)`
3. **`Response` parameter** — FastAPI auto-serializes return model AND attaches cookies set on Response
4. **`FromDishka[Request]`** — works in providers thanks to `FastapiProvider()`
5. **Cookie security** — `httponly=True, secure=True, samesite="lax"`
6. **PyJWT exceptions** — `jwt.ExpiredSignatureError`, `jwt.InvalidTokenError`
7. **Device parsing** — simple UA string checks in interactor (can be enhanced with `user-agents` lib)
8. **`_FRONTEND_` prefix** — note the leading underscore in env prefix for frontend config

## Key File Paths

| What | Path |
|------|------|
| Main app | `src/sport_network_api/main.py` |
| User model (domain) | `src/sport_network_api/domain/user.py` |
| User model (SQLAlchemy) | `src/sport_network_api/infrastructure/models/user.py` |
| User interactor | `src/sport_network_api/application/interactors/user/interactors.py` |
| User controller | `src/sport_network_api/controllers/api/v1/users_controller.py` |
| User schemas | `src/sport_network_api/controllers/schemas/user.py` |
| JWT service | `src/sport_network_api/infrastructure/services/jwt.py` |
| Email service | `src/sport_network_api/infrastructure/services/email.py` |
| TaskIQ broker | `src/sport_network_api/infrastructure/taskiq_broker.py` |
| Auth provider | `src/sport_network_api/ioc/providers/auth.py` |
| IoC setup | `src/sport_network_api/ioc/setup.py` |
| Dockerfile | `Dockerfile` |
| Compose | `compose.yml` |
| Env example | `.env.example` |
