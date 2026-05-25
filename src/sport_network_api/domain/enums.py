from enum import StrEnum


class Gender(StrEnum):
    MAN = "MAN"
    WOMEN = "WOMEN"


class NotificationProvider(StrEnum):
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"
