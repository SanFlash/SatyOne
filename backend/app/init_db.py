"""Initialize the local SatyOne SQLite database and starter catalogue."""
from app.db import Base, engine, SessionLocal
from app import models  # noqa: F401 - register SQLAlchemy models
from app.seed import seed_catalog

def initialize_database() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_catalog(db)

if __name__ == "__main__":
    initialize_database()
    print(f"SatyOne database initialized: {engine.url}")
