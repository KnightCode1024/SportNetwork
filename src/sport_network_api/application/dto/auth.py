from dataclasses import dataclass


@dataclass
class TokenPairDTO:
    access: str
    refresh: str


@dataclass
class AuthDTO:
    user_id: int
    username: str
    email: str
    tokens: TokenPairDTO


@dataclass
class OtpDTO:
    code: str
