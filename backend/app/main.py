from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db import Base,engine,SessionLocal
from app.api.routes import router
from app.seed import seed_catalog

@asynccontextmanager
async def lifespan(app:FastAPI):
    Base.metadata.create_all(bind=engine)
    db=SessionLocal()
    try:seed_catalog(db)
    finally:db.close()
    yield

app=FastAPI(title=settings.app_name,version="0.1.0",description="SatyOne AI Command Intelligence API",lifespan=lifespan)
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.include_router(router,prefix="/api/v1")

@app.get("/")
def root():return {"name":"SatyOne API","status":"online","docs":"/docs"}
@app.get("/health")
def health():return {"status":"healthy"}
