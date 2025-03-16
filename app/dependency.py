from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Annotated
from fastapi import Depends, Header, HTTPException
import uuid, datetime

from config import TOKEN_TTL_SECONDS
from models import Session, Token


async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session, use_cache=True)]

async def get_token(token: Annotated[uuid.UUID, Header()], session: SessionDependency) -> Token:
    query = select(Token).where(
        Token.token == token,
        Token.created_at >= (datetime.datetime.now() - datetime.timedelta(seconds=TOKEN_TTL_SECONDS))
    )
    token = await session.scalar(query)
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

TokenDependency = Annotated[Token, Depends(get_token)]
