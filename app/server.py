from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy import select, and_

from lifespan import lifespan
from schema import (CreateUser, UpdateUser, CreateAdvertisement, UpdateAdvertisement, CreateUserResponse,
                        CreateAdvertisementResponse, Login, LoginResponse, InfoUserResponse)
from dependency import SessionDependency, TokenDependency
from models import User, Advertisement, Token
from crud import add_item, get_item_by_id, delete_item
from constants import SUCCESS_RESPONSE
from auth import hash_password, check_password
from custom_types import Role


app = FastAPI(
    title="Advertisement_API",
    description="API for advertisement",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse(url="/docs")


@app.post("/api/v1/user", tags=["User"], description="Create new user", response_model=CreateUserResponse)
async def create_user(user_data: CreateUser, session: SessionDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = hash_password(user_dict["password"])
    user_orm_obj = User(**user_dict)
    await add_item(session, user_orm_obj)
    return user_orm_obj.id_dict

@app.post("/api/v1/login", tags=["Login"], description="Login", response_model=LoginResponse)
async def login(login_data: Login, session: SessionDependency):
    query = select(User).where(User.username == login_data.username)
    user = await session.scalar(query)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not check_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = Token(user_id=user.id)
    await add_item(session, token)
    return token.dict

@app.get("/api/v1/user/{user_id}", tags=["User"], description="Get user by id", response_model=InfoUserResponse)
async def get_user(user_id: int, session: SessionDependency):
    user_orm_obj = await get_item_by_id(session, User, user_id)
    return user_orm_obj.dict

@app.patch("/api/v1/user/{user_id}", tags=["User"], description="Update user by id")
async def update_user(user_id: int, user_data: UpdateUser, session: SessionDependency, token: TokenDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_dict["password"] = hash_password(user_dict["password"])
    user_orm_obj = await get_item_by_id(session, User, user_id)
    token_user = await session.get(User, token.user_id)
    if token_user.role == Role.ADMIN or user_orm_obj.id == token.user_id:
        for field, value in user_dict.items():
            setattr(user_orm_obj, field, value)
        await add_item(session, user_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=403, detail="Permission denied")

@app.delete("/api/v1/user/{user_id}", tags=["User"], description="Delete user by id")
async def delete_user(user_id: int, session: SessionDependency, token: TokenDependency):
    user_orm_obj = await get_item_by_id(session, User, user_id)
    token_user = await session.get(User, token.user_id)
    if token_user.role == Role.ADMIN or user_orm_obj.id == token.user_id:
        await delete_item(session, user_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=403, detail="Permission denied")


@app.post("/api/v1/advertisement",
          tags=["Advertisement"],
          description="Create new advertisement",
          response_model=CreateAdvertisementResponse)
async def post_advertisement(adv: CreateAdvertisement, session: SessionDependency, token: TokenDependency):
    adv_dict = adv.model_dump(exclude_unset=True)
    adv_orm_obj = Advertisement(**adv_dict, owner_id=token.user_id)
    await add_item(session, adv_orm_obj)
    return adv_orm_obj.dict

@app.get("/api/v1/advertisement/{adv_id}", tags=["Advertisement"], description="Get advertisement by id")
async def get_advertisement(adv_id: int, session: SessionDependency):
    adv_orm_obj = await get_item_by_id(session, Advertisement, adv_id)
    return adv_orm_obj.dict

@app.get("/api/v1/advertisement/", tags=["Advertisement"], description="Search advertisement")
async def search_advertisement(session: SessionDependency, title: str | None = None, description: str | None = None,
                               price: int | None = None):
    query = select(Advertisement)

    filters = []
    if title:
        filters.append(Advertisement.title.ilike(f"%{title}%"))
    if description:
        filters.append(Advertisement.description.ilike(f"%{description}%"))
    if price is not None:
        filters.append(Advertisement.price == price)

    if filters:
        query = query.where(and_(*filters))

    result = await session.execute(query.limit(1000))
    advertisements = result.scalars().all()
    return {"results": [advertisement.dict for advertisement in advertisements]}

@app.patch("/api/v1/advertisement/{adv_id}", tags=["Advertisement"], description="Update advertisement by id")
async def update_advertisement(adv_id: int, adv_data: UpdateAdvertisement, session: SessionDependency, token: TokenDependency):
    adv_dict = adv_data.model_dump(exclude_unset=True)
    adv_orm_obj = await get_item_by_id(session, Advertisement, adv_id)
    token_user = await session.get(User, token.user_id)
    if token_user.role == Role.ADMIN or adv_orm_obj.owner_id == token.user_id:
        for field, value in adv_dict.items():
            setattr(adv_orm_obj, field, value)
        await add_item(session, adv_orm_obj)
        return SUCCESS_RESPONSE
    raise HTTPException(status_code=403, detail="Permission denied")

@app.delete("/api/v1/advertisement/{adv_id}", tags=["Advertisement"], description="Delete advertisement by id")
async def delete_advertisement(adv_id: int, session: SessionDependency, token: TokenDependency):
    adv_orm_obj = await get_item_by_id(session, Advertisement, adv_id)
    token_user = await session.get(User, token.user_id)
    if token_user.role == Role.ADMIN or adv_orm_obj.owner_id == token.user_id:
        await delete_item(session, adv_orm_obj)
        return SUCCESS_RESPONSE
    return HTTPException(status_code=403, detail="Permission denied")
