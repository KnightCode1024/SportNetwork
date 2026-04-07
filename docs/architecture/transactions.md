# Управление транзакциями

## Unit of Work Pattern

Транзакции управляются через паттерн **Unit of Work**, который обеспечивает явные границы транзакций и автоматический commit/rollback.

## Жизненный цикл транзакции

```python
# 1. Dishka создаёт UoW (не enters context)
uow = UnitOfWork(session_factory)

# 2. Dishka создаёт gateways с этим UoW
user_gateway = UserGateway(uow=uow)
profile_gateway = ProfileGateway(uow=uow)

# 3. Dishka создаёт interactor с gateway'ями
interactor = RegisterUserInteractor(
    uow=uow,
    user_repository=user_gateway,
    profile_repository=profile_gateway,
    password_service=password_service,
)

# 4. Controller вызывает interactor
result = await interactor(input_data)
    │
    │  async with self.uow:  ← здесь начинается транзакция
    │      await self.user_repository.create(user)    # использует self.uow.session
    │      await self.profile_repository.create(profile)
    │      # ← при выходе: commit() или rollback()
```

## Реализация

```python
class UnitOfWork(UnitOfWorkInterface):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory
        self._session: AsyncSession | None = None
        self._entered = False


    async def __aenter__(self) -> "UnitOfWork":
        self._session = self.session_factory()
        self._entered = True
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._session is None or not self._entered:
            return
        
        if exc_type is not None:
            await self.rollback()
        else:
            await self.commit()
        
        await self._session.close()
        self._session = None
        self._entered = False
```

## Как использовать в интеракторах

```python
class MyInteractor:
    def __init__(
        self,
        uow: UnitOfWorkInterface,
        repository: SomeGatewayInterface,
    ):
        self.uow = uow
        self.repository = repository
    
    async def __call__(self, data: InputData) -> OutputDTO:
        async with self.uow:  # ← BEGIN
            # Вся бизнес-логика здесь
            entity = await self.repository.create(data)
            
            # Если всё хорошо → commit при выходе
            return self._to_dto(entity)
            # Если exception → rollback автоматически
```

## Преимущества

✅ **Явное управление** - interactor контролирует когда коммитить  
✅ **Автоматический rollback** при ошибках  
✅ **Separation of concerns** - репозитории не коммитят  
✅ **Безопасность** - нельзя забыть commit  
✅ **Тестируемость** - легко мокать UoW interface  

## Важные правила

1. **Interactor** вызывает `async with self.uow:` 
2. **Gateways** используют `self.uow.session` для доступа к сессии
3. **UoW Provider** просто создаёт объект, не enters context
4. **Никогда** не вызывай `session.commit()` из gateway

---

[← Назад к архитектуре](overview.md) | [Порядок выполнения запросов →](request-flow.md)
