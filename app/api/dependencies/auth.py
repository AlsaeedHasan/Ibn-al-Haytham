from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import oauth2_schema, verify_token


async def get_current_user(
    token: str = Depends(oauth2_schema), db_session: AsyncSession = Depends(get_db)
):
    user = verify_token(token, "access", db_session)
    return user
