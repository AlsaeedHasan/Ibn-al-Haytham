import hashlib
import hmac
from datetime import datetime, timedelta, timezone
from typing import Dict, Literal, Optional

import bcrypt
from fastapi import HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.core.config import ALGORITHM, SECRET_KEY
from app.core.helpers import get_token_expiration_minutes

oauth2_schema = OAuth2PasswordBearer(
    "api/v1/auth/token", refreshUrl="api/v1/auth/refresh-token"
)


def hash_password(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(pwd_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def hash_token(token: str) -> str:
    return hmac.new(
        SECRET_KEY.encode("utf-8"), token.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_token(
    data: Dict,
    token_version: int,
    expires_delta: Optional[timedelta] = None,
    token_type: Literal["access", "refresh", "validation", "reset_password"] = "access",
) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=get_token_expiration_minutes(token_type)
        )

    to_encode.update({"exp": expire, "t": token_type, "v": token_version})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


async def verify_token(
    token: str,
    expected_token_type: Literal["access", "refresh", "validation", "reset_password"],
    db_session: AsyncSession,
) -> models.User:
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if expected_token_type != "access":
        revocation_check_stmt = select(models.Token.revoked).where(
            models.Token.token_hash == hash_token(token)
        )
        is_token_revoked = (await db_session.execute(revocation_check_stmt)).scalar()
        if is_token_revoked is True:
            raise credentials_exception

    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
    except JWTError:
        raise credentials_exception

    sub = payload.get("sub", None)
    token_type = payload.get("t", None)

    if not sub or token_type != expected_token_type:
        raise credentials_exception

    token_version = int(payload.get("v", -1))

    user_stmt = select(models.User).where(models.User.id == sub)
    user = (await db_session.execute(user_stmt)).scalar_one_or_none()

    if token_version != user.token_version:
        raise credentials_exception

    return user
