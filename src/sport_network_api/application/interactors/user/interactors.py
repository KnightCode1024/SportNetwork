from dataclasses import dataclass

from sport_network_api.application.dto.user import RegisterUserDTO, UserDTO, LoginUserDTO
from sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sport_network_api.infrastructure.services.password import PasswordService
from sport_network_api.domain.user import User


@dataclass
class RegisterUserInput:
    username: str
    email: str
    password: str


@dataclass
class LoginUserInput:
    username: str
    password: str


class RegisterUserInteractor:
    def __init__(
        self,
        user_repository: UserGatewayInterface,
        password_service: PasswordService,
    ):
        self.user_repository = user_repository
        self.password_service = password_service
    
    async def __call__(self, input_data: RegisterUserInput) -> RegisterUserDTO:
        existing_user_by_email = await self.user_repository.get_by_email(input_data.email)
        if existing_user_by_email:
            raise ValueError(f"Email '{input_data.email}' уже занят")
        existing_user_by_username = await self.user_repository.get_by_username(input_data.username)
        if existing_user_by_username:
            raise ValueError(f"Username '{input_data.username}' уже занят")
        password_hash = self.password_service.hash_password(input_data.password)
        user = User(
            id=None,
            username=input_data.username,
            email=input_data.email,
            password_hash=password_hash,
            is_active=False,
        )
        created_user = await self.user_repository.create(user)
        return self._to_dto(created_user)
    
    def _to_dto(self, user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )


class LoginUserInteractor:
    def __init__(self, user_repository: UserGatewayInterface):
        self.user_repository = user_repository
    
    async def __call__(self, input_data: LoginUserInput) -> LoginUserDTO:
        raise NotImplementedError("LoginUserInteractor not implemented yet")


class GetUserInteractor:
    def __init__(self, user_repository: UserGatewayInterface):
        self.user_repository = user_repository
    
    async def __call__(self, user_id: int) -> UserDTO:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return self._to_dto(user)
    
    def _to_dto(self, user: User) -> UserDTO:
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
        )
