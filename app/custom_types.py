from enum import Enum


class Role(str, Enum):
    ADMIN = 1
    USER = 2
