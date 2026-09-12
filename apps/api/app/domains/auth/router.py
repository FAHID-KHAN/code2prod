from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.db import get_db
from app.core.rate_limit import rate_limit
from app.domains.auth import service
from app.domains.auth.dependencies import get_current_user
from app.domains.auth.models import User
from app.domains.auth.schemas import (
    LoginRequest,
    MessageOut,
    PasswordResetConfirm,
    PasswordResetRequest,
    RegisterRequest,
    TokenPair,
    UserOut,
    VerifyEmailRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])

REFRESH_COOKIE = "code2prod_refresh"

# Generic so a caller cannot tell a malformed token from someone else's valid one.
_GENERIC_SUCCESS = "If that email address has an account, we've sent instructions to it."


def _set_refresh_cookie(response: Response, tokens: service.IssuedTokens) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE,
        value=tokens.refresh_token,
        httponly=True,
        # Strict is what defends the cookie-based refresh endpoint from CSRF;
        # the access token travels in a header and is unaffected.
        samesite="strict",
        secure=settings.is_production,
        max_age=settings.refresh_token_ttl_days * 24 * 60 * 60,
        path="/auth",
    )


def _read_refresh_token(request: Request) -> str:
    # Cookie first for browsers; body/header fallback keeps native clients viable
    # without a second code path.
    token = request.cookies.get(REFRESH_COOKIE) or request.headers.get("x-refresh-token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing refresh token"
        )
    return token


def _to_token_pair(tokens: service.IssuedTokens) -> TokenPair:
    return TokenPair(access_token=tokens.access_token, expires_at=tokens.access_expires_at)


@router.post(
    "/register",
    response_model=MessageOut,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[rate_limit(limit=5, window_seconds=3600)],
)
def register(payload: RegisterRequest, db: Session = Depends(get_db)) -> MessageOut:
    service.register(db, payload.email, payload.password, payload.display_name)
    return MessageOut(detail=_GENERIC_SUCCESS)


@router.post(
    "/verify-email",
    response_model=MessageOut,
    dependencies=[rate_limit(limit=10, window_seconds=3600)],
)
def verify_email(payload: VerifyEmailRequest, db: Session = Depends(get_db)) -> MessageOut:
    try:
        service.verify_email(db, payload.token)
    except service.AuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    return MessageOut(detail="Email verified. You can sign in now.")


@router.post(
    "/login",
    response_model=TokenPair,
    dependencies=[rate_limit(limit=10, window_seconds=900)],
)
def login(
    payload: LoginRequest, response: Response, db: Session = Depends(get_db)
) -> TokenPair:
    try:
        tokens = service.login(db, payload.email, payload.password)
    except service.AuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    _set_refresh_cookie(response, tokens)
    return _to_token_pair(tokens)


@router.post(
    "/refresh",
    response_model=TokenPair,
    dependencies=[rate_limit(limit=60, window_seconds=900)],
)
def refresh(request: Request, response: Response, db: Session = Depends(get_db)) -> TokenPair:
    try:
        tokens = service.refresh(db, _read_refresh_token(request))
    except service.AuthError as exc:
        response.delete_cookie(REFRESH_COOKIE, path="/auth")
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc

    _set_refresh_cookie(response, tokens)
    return _to_token_pair(tokens)


@router.post("/logout", response_model=MessageOut)
def logout(request: Request, response: Response, db: Session = Depends(get_db)) -> MessageOut:
    token = request.cookies.get(REFRESH_COOKIE) or request.headers.get("x-refresh-token")
    if token:
        service.logout(db, token)
    response.delete_cookie(REFRESH_COOKIE, path="/auth")
    return MessageOut(detail="Signed out.")


@router.post(
    "/password-reset/request",
    response_model=MessageOut,
    status_code=status.HTTP_202_ACCEPTED,
    dependencies=[rate_limit(limit=5, window_seconds=3600)],
)
def request_password_reset(
    payload: PasswordResetRequest, db: Session = Depends(get_db)
) -> MessageOut:
    service.request_password_reset(db, payload.email)
    return MessageOut(detail=_GENERIC_SUCCESS)


@router.post(
    "/password-reset/confirm",
    response_model=MessageOut,
    dependencies=[rate_limit(limit=10, window_seconds=3600)],
)
def confirm_password_reset(
    payload: PasswordResetConfirm, db: Session = Depends(get_db)
) -> MessageOut:
    try:
        service.confirm_password_reset(db, payload.token, payload.password)
    except service.AuthError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    return MessageOut(detail="Password updated. All existing sessions were signed out.")


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)) -> User:
    return user
