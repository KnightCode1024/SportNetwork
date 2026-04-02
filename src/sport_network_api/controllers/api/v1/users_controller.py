from fastapi import APIRouter, status, HTTPException
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from sport_network_api.application.interactors.user.interactors import (
    RegisterUserInteractor,
    RegisterUserInput,
    LoginUserInteractor,
    GetUserInteractor,
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


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    route_class=DishkaRoute,
)


@router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest,
    interactor: FromDishka[RegisterUserInteractor],
) -> RegisterResponse:
    try:
        input_data = RegisterUserInput(
            username=request.username,
            email=request.email,
            password=request.password,
        )
        res = await interactor(input_data)
        return RegisterResponse(
            id=res.id,
            username=res.username,
            email=res.email,
            is_active=res.is_active,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}",
        )


@router.get("/verify-email")
async def verify_email(token: str):
    pass


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    interactor: FromDishka[LoginUserInteractor],
) -> LoginResponse:
    pass


@router.post("check-code")
async def check_code():
    pass


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: FromDishka[UserResponse]
) -> UserResponse:
    return current_user
