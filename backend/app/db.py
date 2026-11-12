from pathlib import Path
from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

# SQLite is the default and authoritative local database.
# Keep the file in backend/data so starting the app from another working
# directory does not silently create a second database.
BACKEND_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_DATABASE_URL = f"sqlite:///{(DATA_DIR / 'satyone.db').as_posix()}"
DATABASE_URL = (settings.database_url.strip() if settings.database_url and settings.database_url.strip() else DEFAULT_DATABASE_URL)

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False, "timeout": 30}
else:
    connect_args = {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

if DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def configure_sqlite(dbapi_connection, _connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=30000")
        cursor.close()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
