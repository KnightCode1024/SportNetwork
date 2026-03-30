class AuthenticationError(Exception):
    pass


class UserAlreadyExistsError(AuthenticationError):
    pass


class InvalidCredentialsError(AuthenticationError):
    pass


class UserNotFoundError(AuthenticationError):
    pass
