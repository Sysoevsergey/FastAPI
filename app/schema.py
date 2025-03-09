from pydantic import BaseModel, field_validator


class UserValidation:
    @field_validator("password", check_fields=False, mode="before")
    def password_length(cls, value):
        if len(value) < 8:
            raise ValueError("Пароль должен быть не менее 8 символов")
        return value

    @field_validator("name", check_fields=False, mode="before")
    def name_length(cls, value):
        if not value:
            raise ValueError("Имя не может быть пустым")
        return value

class User(BaseModel, UserValidation):
    pass

class CreateUser(User):
    name: str
    password: str

class CreateUserResponse(User):
    id: int
    name: str
    created_at: str

class UpdateUser(User):
    name: str | None = None
    password: str | None = None



class AdvertisementValidation:
    @field_validator("title", check_fields=False, mode="before")
    def title_length(cls, value):
        if not value:
            raise ValueError("Заголовок не может быть пустым")
        return value

    @field_validator("description", check_fields=False, mode="before")
    def description_length(cls, value):
        if not value:
            raise ValueError("Описание не может быть пустым")
        return value

    @field_validator("price", check_fields=False, mode="before")
    def price_value(cls, value):
        if value < 0:
            raise ValueError("Цена не может быть отрицательной")
        return value

class Advertisement(BaseModel, AdvertisementValidation):
    pass


class CreateAdvertisement(Advertisement):
    title: str
    description: str
    price: int
    owner_id: int

class CreateAdvertisementResponse(Advertisement):
    id: int
    title: str
    description: str
    price: int
    owner_id: int
    created_at: str

class UpdateAdvertisement(Advertisement):
    title: str | None = None
    description: str | None = None
    price: int | None = None
