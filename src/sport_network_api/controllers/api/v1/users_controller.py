from fastapi import APIRouter, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from sport_network_api.application.interactors.user.interactors import (
    RegisterUserInteractor,
    LoginUserInteractor,
    GetUserInteractor,
)
from sport_network_api.application.interactors.user.input import (
    RegisterUserInput,
    LoginUserInput,
)
from sport_network_api.application.interactors.user.errors import (
    AuthenticationError,
    UserAlreadyExistsError,
    InvalidCredentialsError,
    UserNotFoundError,
)
from sport_network_api.controllers.schemas.user import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    RegisterResponse,
    LoginResponse,
    ErrorResponse,
)


controller = APIRouter(prefix="/users", tags=["Users"], route_class=DishkaRoute)


@controller.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest,
    # interactor: RegisterUserInteractor = DishkaDepends(),
):
    pass

@controller.get("/verify-email")
async def verify_email(token: str):
    pass

@controller.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    # interactor: LoginUserInteractor = DishkaDepends(),
):
    pass

@controller.post("check-code")
async def check_code():
    pass

@controller.get("/me")
async def get_me(
    current_user: FromDishka[UserResponse]
):
    return current_user
