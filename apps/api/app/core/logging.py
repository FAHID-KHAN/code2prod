import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

_RESERVED = frozenset(
    logging.LogRecord("", 0, "", 0, "", None, None).__dict__
) | {"message", "asctime", "taskName"}


class JsonFormatter(logging.Formatter):
    """Renders one JSON object per line so logs stay queryable in aggregation."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        request_id = request_id_var.get()
        if request_id is not None:
            payload["request_id"] = request_id

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        for key, value in record.__dict__.items():
            if key not in _RESERVED:
                payload[key] = value

        return json.dumps(payload, default=str)


def configure_logging(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)

    # uvicorn installs its own handlers; drop them so every line is JSON.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = True


def register_exception_logging(app: FastAPI) -> None:
    """Log unhandled exceptions with request context.

    This is the seam an error-tracking provider (Sentry et al.) plugs into later —
    it deliberately does not depend on one yet.
    """
    logger = logging.getLogger("app.unhandled")

    @app.exception_handler(Exception)
    async def _handle(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "unhandled exception",
            extra={"path": request.url.path, "method": request.method},
        )
        return JSONResponse(status_code=500, content={"detail": "Internal server error"})
