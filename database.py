from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

SQLALCHEMY_DATABASE_URL = "https://app.netlify.com/projects/crtlshift/database"

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
