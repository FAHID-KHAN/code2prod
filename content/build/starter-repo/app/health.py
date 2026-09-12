from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    # BYTE-103: this is intentionally wrong — Mission 3 fixes it.
    return {"status": "not implemented"}
