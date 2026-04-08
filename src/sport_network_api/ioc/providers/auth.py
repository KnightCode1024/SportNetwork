from dishka import Provider, Scope, provide
from fastapi import Request, HTTPException, status
from jwt import ExpiredSignatureError, InvalidTokenError

from sport_network_api.application.interfaces.gateways.user_gateway import UserGatewayInterface
from sport_network_api.application.interfaces.gateways.token_blacklist_gateway import TokenBlacklistGatewayInterface
from sport_network_api.application.interfaces.services.jwt_service import JwtServiceInterface
from sport_network_api.application.interactors.user.interactors import GetUserInteractor
from sport_network_api.controllers.schemas.user import UserResponse



class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    async def get_current_user(
        self,
        get_user: GetUserInteractor,
        jwt_service: JwtServiceInterface,
        token_blacklist_gateway: TokenBlacklistGatewayInterface,
        request: Request,
    ) -> UserResponse:
        authorization = request.headers.get("Authorization")
        token: str | None = None

        if authorization:
            try:
                scheme, token = authorization.split()
                if scheme.lower() != "bearer":
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid authentication scheme",
                    )

            except ValueError as err:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header",
                ) from err
        else:
            token = request.cookies.get("access_token")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization token missing",
            )

        if await token_blacklist_gateway.is_blacklisted(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
            )

        try:
            decoded_token  = jwt_service.decode_jwt(token)
        except InvalidTokenError as err:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            ) from err

        user_id = int(decoded_token.get("sub"))

        user = await get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )

        return UserResponse(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
        )