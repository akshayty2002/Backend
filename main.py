import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from database import engine, Base

# Import the explicit router files directly from the folder
from router import auth, listings, messages

Base.metadata.create_all(bind=engine)


def _migrate_legacy_schema():
    """
    Older copies of database.db may predate the created_at column added to
    the Listing model. SQLAlchemy's create_all() only creates missing
    tables, not missing columns on existing tables, so we patch it in here
    if needed. Safe to run every startup — it's a no-op once the column
    exists.
    """
    conn = sqlite3.connect(settings.DB_FILE)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(listings)")
    columns = {row[1] for row in cur.fetchall()}
    if "created_at" not in columns:
        cur.execute("ALTER TABLE listings ADD COLUMN created_at TIMESTAMP")
        conn.commit()
    conn.close()


_migrate_legacy_schema()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pass the direct router object attributes to FastAPI
app.include_router(auth.router)
app.include_router(listings.router)
app.include_router(messages.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok", "version": settings.VERSION}
