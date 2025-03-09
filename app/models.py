from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.schema import ForeignKey
import datetime

from app.config import PG_DSN


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
    name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    advertisements = relationship("Advertisement", back_populates="owner")

    @property
    def dict(self):
        return {"id": self.id,
                "name": self.name,
                "created_at": self.created_at.isoformat()}

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

ORM_OBJ = User, Advertisement
ORM_CLS = type[User, Advertisement]


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()
