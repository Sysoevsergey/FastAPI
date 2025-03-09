from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from sqlalchemy import select, and_

from app.lifespan import lifespan
from app.schema import (CreateUser, UpdateUser, CreateAdvertisement, UpdateAdvertisement, CreateUserResponse,
                        CreateAdvertisementResponse)
from app.dependency import SessionDependency
from app.models import User, Advertisement
from app.crud import add_item, get_item_by_id, delete_item
from app.constants import SUCCESS_RESPONSE


app = FastAPI(
    title="Advertisement_API",
    description="API for advertisement",
    lifespan=lifespan,
)


@app.get("/", include_in_schema=False)
async def home():
    return RedirectResponse(url="/docs")


@app.post("/api/v1/user", tags=["User"], description="Create new user", response_model=CreateUserResponse)
async def post_user(user: CreateUser, session: SessionDependency):
    user_dict = user.model_dump(exclude_unset=True)
    user_orm_obj = User(**user_dict)
    await add_item(session, user_orm_obj)
    return user_orm_obj.dict

@app.get("/api/v1/user/{id}", tags=["User"], description="Get user by id")
async def get_user(user_id: int, session: SessionDependency):
    user_orm_obj = await get_item_by_id(session, User, user_id)
    return user_orm_obj.dict

@app.patch("/api/v1/user/{id}", tags=["User"], description="Update user by id")
async def update_user(user_id: int, user_data: UpdateUser, session: SessionDependency):
    user_dict = user_data.model_dump(exclude_unset=True)
    user_orm_obj = await get_item_by_id(session, User, user_id)
    for field, value in user_dict.items():
        setattr(user_orm_obj, field, value)
    await add_item(session, user_orm_obj)
    return SUCCESS_RESPONSE

@app.delete("/api/v1/user/{id}", tags=["User"], description="Delete user by id")
async def delete_user(user_id: int, session: SessionDependency):
    user_orm_obj = await get_item_by_id(session, User, user_id)
    await delete_item(session, user_orm_obj)
    return SUCCESS_RESPONSE


@app.post("/api/v1/advertisement",
          tags=["Advertisement"],
          description="Create new advertisement",
          response_model=CreateAdvertisementResponse)
async def post_advertisement(adv: CreateAdvertisement, session: SessionDependency):
    adv_dict = adv.model_dump(exclude_unset=True)
    adv_orm_obj = Advertisement(**adv_dict)
    await add_item(session, adv_orm_obj)
    return adv_orm_obj.dict

@app.get("/api/v1/advertisement/{id}", tags=["Advertisement"], description="Get advertisement by id")
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

@app.patch("/api/v1/advertisement/{id}", tags=["Advertisement"], description="Update advertisement by id")
async def update_advertisement(adv_id: int, adv_data: UpdateAdvertisement, session: SessionDependency):
    adv_dict = adv_data.model_dump(exclude_unset=True)
    adv_orm_obj = await get_item_by_id(session, Advertisement, adv_id)
    for field, value in adv_dict.items():
        setattr(adv_orm_obj, field, value)
    await add_item(session, adv_orm_obj)
    return SUCCESS_RESPONSE

@app.delete("/api/v1/advertisement/{id}", tags=["Advertisement"], description="Delete advertisement by id")
async def delete_advertisement(adv_id: int, session: SessionDependency):
    adv_orm_obj = await get_item_by_id(session, Advertisement, adv_id)
    await delete_item(session, adv_orm_obj)
    return SUCCESS_RESPONSE
