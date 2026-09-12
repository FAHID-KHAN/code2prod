"""Fixed-window rate limiting for authentication endpoints (§20).

Deliberately in-process: §17 says not to introduce Redis before a real need
appears. The limits therefore apply per API instance and reset on deploy, which
is adequate for a single-instance launch and must move to a shared store before
the API is scaled horizontally or put behind more than one replica.
"""

import threading
import time
from collections import defaultdict

from fastapi import HTTPException, Request, status
from fastapi import params as fastapi_params


class FixedWindowLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, list[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def check(self, key: str, limit: int, window_seconds: int) -> bool:
        now = time.monotonic()
        cutoff = now - window_seconds

        with self._lock:
            hits = [stamp for stamp in self._hits[key] if stamp > cutoff]
            if len(hits) >= limit:
                self._hits[key] = hits
                return False
            hits.append(now)
            self._hits[key] = hits
            return True

    def reset(self) -> None:
        with self._lock:
            self._hits.clear()


limiter = FixedWindowLimiter()


def rate_limit(limit: int, window_seconds: int) -> fastapi_params.Depends:
    def dependency(request: Request) -> None:
        client = request.client.host if request.client else "unknown"
        key = f"{request.url.path}:{client}"
        if not limiter.check(key, limit, window_seconds):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Try again later.",
            )

    return fastapi_params.Depends(dependency)
