from enum import Enum


class Gender(Enum):
    MAN = "man"
    WOMEN = "women"


class NotificationProvider(Enum):
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"
