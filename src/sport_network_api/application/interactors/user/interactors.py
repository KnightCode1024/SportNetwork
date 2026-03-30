import bcrypt
from datetime import datetime
from uuid import UUID, uuid4

from sport_network_api.domain.user import User
from src.sport_network_api.application.interfaces.user_gateway import UserGatewayInterface
from sport_network_api.application.interactors.user.input import RegisterUserInput, LoginUserInput
from sport_network_api.application.dto.user import UserDTO, RegisterUserDTO, LoginUserDTO
from src.sport_network_api.application.interactors.user.errors import (
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)


class RegisterUserInteractor:
    def __init__(self, user_repository: UserGatewayInterface):
        self.user_repository = user_repository

    async def __call__(self, input_data: RegisterUserInput) -> RegisterUserDTO:
        pass


class LoginUserInteractor:
    def __init__(self, user_repository: UserGatewayInterface):
        self.user_repository = user_repository

    async def __call__(self, input_data: LoginUserInput) -> LoginUserDTO:
        pass


class GetUserInteractor:
    def __init__(self, user_repository: UserGatewayInterface):
        self.user_repository = user_repository

    async def __call__(self, user_id: int) -> UserDTO:
        pass
