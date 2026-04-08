# Ключевые компоненты

## Domain Models (`src/domain/`)

Чистые бизнес-объекты без зависимостей от фреймворков. Содержат бизнес-правила и поведение.

```python
# domain/user.py
class User:
    def verify_password(self, password: str) -> bool: ...
    def activate(self) -> None: ...
    def deactivate(self) -> None: ...

# domain/profile.py
class Profile:
    def update_bio(self, bio: str) -> None:  # validation
    def set_age(self, age: int) -> None:     # validation 14-120
```

## Interfaces (`src/application/interfaces/`)

Протоколы (абстракции), которые определяют контракты для внешней инфраструктуры.

```python
class UserGatewayInterface(Protocol):
    async def get_by_id(self, user_id: int) -> User | None: ...
    async def create(self, user: User) -> User: ...

class UnitOfWorkInterface(Protocol):
    async def __aenter__(self) -> "UnitOfWorkInterface": ...
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None: ...
```

## Interactors (`src/application/interactors/`)

Бизнес-юзы. Координируют работу domain моделей, gateways и сервисов. Управляют транзакциями.

```python
class RegisterUserInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,          # ← управление транзакцией
        user_repository: UserGatewayInterface,
        profile_repository: ProfileGatewayInterface,
        password_service: PasswordServiceInterface,
    ): ...
    
    async def __call__(self, input_data: RegisterUserInput) -> RegisterUserDTO:
        async with self.uow:  # ← явная граница транзакции
            # ... бизнес-логика
```

## Gateways (`src/infrastructure/gateways/`)

Реализация интерфейсов для работы с БД. Маппят domain ↔ SQLAlchemy models.

```python
class UserGateway(UserGatewayInterface):
    def __init__(self, uow: UnitOfWorkInterface):
        self.uow = uow  # ← session берётся из UoW
    
    async def create(self, user: User) -> User:
        user_model = self._from_domain(user)
        self.uow.session.add(user_model)  # ← session из UoW
        await self.uow.session.flush()
        return self._to_domain(user_model)
```

## Unit of Work (`src/infrastructure/unit_of_work.py`)

Управляет транзакциями. Interactor явно начинает и заканчивает транзакцию.

```python
class UnitOfWork(UnitOfWorkInterface):
    async def __aenter__(self):
        self._session = self.session_factory()  # BEGIN
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()  # ROLLBACK
        else:
            await self.commit()    # COMMIT
        await self._session.close()
```

## DI Container (`src/ioc/`)

Dishka собирает все зависимости при старте приложения.

```
Scope.APP (singleton):
  • DatabaseConfig
  • async_sessionmaker
  • PasswordService

Scope.REQUEST (per request):
  • UnitOfWork
  • UserGateway
  • ProfileGateway
  • RegisterUserInteractor
```

---

[← Назад к архитектуре](overview.md) | [Управление транзакциями →](transactions.md)
