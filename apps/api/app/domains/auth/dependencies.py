from collections.abc import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.security import decode_access_token
from app.domains.auth.models import Role, User

# auto_error=False so a missing header produces our own 401 rather than a 403.
_bearer = HTTPBearer(auto_error=False)

_CREDENTIALS_ERROR = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise _CREDENTIALS_ERROR

    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise _CREDENTIALS_ERROR

    try:
        user_id = int(payload["sub"])
    except (KeyError, TypeError, ValueError):
        raise _CREDENTIALS_ERROR from None

    # The role is re-read from the database rather than trusted from the token, so
    # a demotion takes effect immediately instead of at token expiry.
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise _CREDENTIALS_ERROR
    return user


def require_role(*roles: Role) -> Callable[[User], User]:
    """Authorisation enforced in the API, never merely hidden in the UI (§20)."""
    allowed = frozenset(roles)

    def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return user

    return dependency
