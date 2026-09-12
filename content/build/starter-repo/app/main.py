from fastapi import FastAPI

from app.health import router as health_router

app = FastAPI(title="ByteBangla API")
app.include_router(health_router)


@app.get("/")
def root():
    return {"message": "ByteBangla API"}
