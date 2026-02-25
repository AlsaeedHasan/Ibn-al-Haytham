from typing import Literal

from app.core.config import (
    ACCESS_TOKEN_EXPIRES_MINUTES,
    ACCOUNT_PROCCESS_EXPIRES_MINUTES,
    REFRESH_TOKEN_EXPIRES_MINUTES,
)


def get_token_expiration_minutes(
    token_type: Literal[
        "access", "refresh", "verification", "password_reset"
    ] = "access",
) -> int:
    match token_type:
        case "access":
            return ACCESS_TOKEN_EXPIRES_MINUTES
        case "refresh":
            return REFRESH_TOKEN_EXPIRES_MINUTES
        case "verification" | "password_reset":
            return ACCOUNT_PROCCESS_EXPIRES_MINUTES
        case _:
            return 15
