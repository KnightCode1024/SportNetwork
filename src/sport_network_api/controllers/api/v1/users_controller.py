from fastapi import APIRouter, Request, Response, Query, HTTPException, status
from dishka.integrations.fastapi import FromDishka, DishkaRoute

from sport_network_api.application.interactors.user.interactors import (
    RegisterUserInteractor,
    LoginUserInteractor,
    GetUserInteractor,
    VerifyEmailInteractor,
    RequestPasswordResetInteractor,
    ConfirmPasswordResetInteractor,
    LogoutUserInteractor,
    LoginDeviceInfo,
)
from sport_network_api.application.dto.user import (
    RegisterUserInput,
    LoginUserInput,
    VerifyEmailInput,
    ResetPasswordInput,
    ResetPasswordConfirmInput,
    LogoutUserInput,
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
    ResetPasswordRequest,
    ResetPasswordConfirmRequest,
    ResetPasswordResponse,
)
from sport_network_api.config.auth_jwt import AuthJWTConfig


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    route_class=DishkaRoute,
)


def set_auth_cookies(
    response: Response,
    access_token: str,
    refresh_token: str,
    jwt_config: AuthJWTConfig,
) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=jwt_config.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=jwt_config.REFRESH_TOKEN_EXPIRE_DAYS * 86400,
    )


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax",
    )


@router.post("/register", response_model=RegisterResponse)
async def register(
    request: RegisterRequest,
    register_user: FromDishka[RegisterUserInteractor],
    response: Response,
) -> RegisterResponse:
    input_data = RegisterUserInput(
        username=request.username,
        email=request.email,
        password=request.password,
        date_of_birth=request.date_of_birth,
        gender=request.gender.value if request.gender else None,
    )
    try:
        result = await register_user(input_data)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return RegisterResponse(
        id=result.id,
        username=result.username,
        email=result.email,
        is_active=result.is_active,
    )


@router.get("/verify-email")
async def verify_email(
    interactor: FromDishka[VerifyEmailInteractor],
    token: str = Query(...),
) -> dict[str, bool]:
    input_data = VerifyEmailInput(token=token)
    try:
        await interactor(input_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"verified": True}


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    response: Response,
    input_data: LoginRequest,
    interactor: FromDishka[LoginUserInteractor],
    jwt_config: FromDishka[AuthJWTConfig],
) -> LoginResponse:
    forwarded_for = request.headers.get("X-Forwarded-For", "")
    ip_address = forwarded_for.split(",")[0].strip() if forwarded_for else request.client.host
    user_agent = request.headers.get("User-Agent", "")

    login_input = LoginUserInput(
        identifier=input_data.identifier,
        password=input_data.password,
    )
    device_info = LoginDeviceInfo(
        ip_address=ip_address,
        user_agent=user_agent,
    )

    try:
        res = await interactor(login_input, device_info)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    set_auth_cookies(
        response,
        res.access_token,
        res.refresh_token,
        jwt_config)

    return LoginResponse(
        access_token=res.access_token,
        refresh_token=res.refresh_token,
    )

@router.post("/refresh")
async def refresh_token():
    pass

@router.post("/check-code")
async def check_code():
    pass

@router.get("/resend-code")
async def resend_code():
    pass


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: FromDishka[UserResponse]
) -> UserResponse:
    return current_user


@router.post("/reset-password", response_model=ResetPasswordResponse)
async def reset_password(
    request: ResetPasswordRequest,
    interactor: FromDishka[RequestPasswordResetInteractor],
) -> ResetPasswordResponse:
    input_data = ResetPasswordInput(email=request.email)
    await interactor(input_data)
    return ResetPasswordResponse(success=True)


@router.post("/reset-password/confirm", response_model=ResetPasswordResponse)
async def reset_password_confirm(
    request: ResetPasswordConfirmRequest,
    interactor: FromDishka[ConfirmPasswordResetInteractor],
) -> ResetPasswordResponse:
    input_data = ResetPasswordConfirmInput(
        token=request.token,
        new_password=request.new_password,
    )
    try:
        await interactor(input_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return ResetPasswordResponse(success=True)

@router.post("/logout")
async def logout(
    request: Request,
    response: Response,
    current_user: FromDishka[UserResponse],
    interactor: FromDishka[LogoutUserInteractor],
) -> dict[str, str]:
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
    
    authorization = request.headers.get("Authorization")
    if authorization and not access_token:
        try:
            scheme, access_token = authorization.split()
        except ValueError:
            pass
    
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No token to logout",
        )
    
    logout_input = LogoutUserInput(
        access_token=access_token,
        refresh_token=refresh_token,
    )
    await interactor(logout_input)
    
    clear_auth_cookies(response)
    
    return {"message": "Successfully logged out"}
