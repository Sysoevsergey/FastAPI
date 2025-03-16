from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, UUID, func
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.schema import ForeignKey
import datetime, uuid

from config import PG_DSN
from custom_types import Role


engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    @property
    def id_dict(self):
        return {"id": self.id}


class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=False)
    advertisements = relationship("Advertisement", back_populates="owner")
    tokens: Mapped[list["Token"]] = relationship("Token", back_populates="user")
    role: Mapped[Role] = mapped_column(ENUM(Role), nullable=False, default=Role.USER)

    @property
    def dict(self):
        return {"id": self.id,
                "user_name": self.username,
                "name": self.name,
                "created_at": self.created_at.isoformat()}


class Token(Base):
    __tablename__ = "tokens"
    token: Mapped[uuid] = mapped_column(UUID, nullable=False, server_default=func.gen_random_uuid())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped[User] = relationship("User", back_populates="tokens")

    @property
    def dict(self):
        return {"token": self.token}


class Advertisement(Base):
    __tablename__ = "advertisements"
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    owner: Mapped[User] = relationship("User", back_populates="advertisements")

    @property
    def dict(self):
        return {"id": self.id,
                "title": self.title,
                "description": self.description,
                "price": self.price,
                "owner_id": self.owner_id,
                "created_at": self.created_at.isoformat()}


ORM_OBJ = User | Advertisement | Token
ORM_CLS = type[User], type[Advertisement], type[Token]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()
