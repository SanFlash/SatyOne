from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db import Base, engine, SessionLocal
from app import models  # noqa: F401
from app.api.routes import router
from app.seed import seed_catalog

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables and seed the catalogue once at startup. SQLite is stored
    # under backend/data/satyone.db by default.
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_catalog(db)
    yield

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="SatyOne — local-first AI command intelligence workspace",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)
app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"name": "SatyOne API", "status": "online", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy", "database": "sqlite" if engine.dialect.name == "sqlite" else engine.dialect.name}

@app.get("/api/v1/system")
def system_info():
    return {
        "app": "SatyOne",
        "version": "1.0.0",
        "database": engine.dialect.name,
        "local_first": engine.dialect.name == "sqlite",
        "status": "ready",
    }
