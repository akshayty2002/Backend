from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Render (and most hosts) inject a DATABASE_URL env var when you attach a
# Postgres database — use it if present. Falls back to local SQLite for
# local development, where a persistent Postgres instance usually isn't
# worth the setup.
#
# IMPORTANT: SQLite on Render's free tier lives on ephemeral disk storage —
# it resets to whatever was last deployed every time the service restarts
# or wakes from sleep. Postgres (via DATABASE_URL) is durable and doesn't
# have this problem, which is why production should always use it.
_database_url = settings.DATABASE_URL

if _database_url:
    # Render's DATABASE_URL sometimes starts with "postgres://", but
    # SQLAlchemy 1.4+ requires the "postgresql://" scheme.
    if _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URL = _database_url
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
else:
    SQLALCHEMY_DATABASE_URL = f"sqlite:///./{settings.DB_FILE}"
    # connect_args={"check_same_thread": False} is required specifically for SQLite
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Yields a transactional database session that automatically closes on completion."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
