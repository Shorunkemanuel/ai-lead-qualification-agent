from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import initialize_database
from app.routes import router as leads_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    initialize_database()
    yield

app = FastAPI(
    title="AI Lead Qualification Agent",
    version="0.1.0",
    lifespan=lifespan,
)
app.include_router(leads_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
