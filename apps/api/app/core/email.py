"""Outbound email.

Phase 1 needs to deliver verification and reset tokens; a real transactional
provider arrives with the rest of notifications (blueprint §11, §15). Until then
messages are logged, so the flows are fully exercisable without a vendor.
"""

import logging

logger = logging.getLogger("app.email")


def send_email(to: str, subject: str, body: str) -> None:
    logger.info(
        "email dispatched",
        extra={"to": to, "subject": subject, "body": body},
    )
