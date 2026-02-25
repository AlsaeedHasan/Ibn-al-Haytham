from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app import models
from fastapi import HTTPException, status
from app.core.helpers import get_token_expiration_minutes
from app.core.security import create_token, hash_token, verify_password, verify_token


class AuthService:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.authentication_error = HTTPException(
            status.HTTP_401_UNAUTHORIZED, "User not found or incorrect password."
        )
        self.data_integrity_error = HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR, "Data integrity error."
        )
        self.user = None

    async def authenticate_student(
        self,
        student_code: str,
        password: str,
    ) -> models.Student | None:

        stmt = (
            select(models.Student)
            .options(joinedload(models.Student.user))
            .where(models.Student.student_code == student_code)
        )
        result = await self.db_session.execute(stmt)
        stu = result.scalar()

        if not stu or not verify_password(password, stu.user.hashed_password):
            raise self.authentication_error

        return stu

    async def authenticate_staff(
        self,
        university_email: str,
        password: str,
    ) -> models.User | None:

        stmt = select(models.User).where(
            models.User.university_email == university_email
        )
        result = await self.db_session.execute(stmt)
        staff = result.scalar()

        if not staff or not verify_password(password, staff.hashed_password):
            raise self.authentication_error

        return staff

    async def generate_tokens(
        self,
        user: models.User,
        access_token_expiration_minutes: Optional[int] = None,
        refresh_token_expiration_minutes: Optional[int] = None,
    ) -> Dict:
        actual_refresh_minutes = (
            refresh_token_expiration_minutes or get_token_expiration_minutes("refresh")
        )
        refresh_expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=actual_refresh_minutes
        )

        access_token = create_token(
            {"sub": str(user.id)},
            token_version=user.token_version,
            token_type="access",
            expires_delta=(
                timedelta(minutes=access_token_expiration_minutes)
                if access_token_expiration_minutes
                else None
            ),
        )

        refresh_token = create_token(
            {"sub": str(user.id)},
            token_version=user.token_version,
            token_type="refresh",
            expires_delta=(
                timedelta(minutes=refresh_token_expiration_minutes)
                if refresh_token_expiration_minutes
                else None
            ),
        )

        hashed_refresh_token = hash_token(refresh_token)

        await self.db_session.add(
            models.Token(
                token_hash=hashed_refresh_token,
                user_id=user.id,
                expires_at=refresh_expires_at,
            )
        )

        try:
            await self.db_session.commit()
        except IntegrityError:
            await self.db_session.rollback()
            raise self.data_integrity_error

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def refresh_user_tokens(self, refresh_token: str) -> Dict:
        stmt = select(models.Token).where(
            models.Token.token_hash == hash_token(refresh_token)
        )
        db_token = (await self.db_session.execute(stmt)).scalar()

        if not db_token or db_token.revoked:
            raise self.authentication_error

        user = await verify_token(refresh_token, "refresh", self.db_session)

        db_token.revoked = True
        try:
            await self.db_session.flush()
        except IntegrityError:
            await self.db_session.rollback()
            raise self.data_integrity_error

        return await self.generate_tokens(user)
