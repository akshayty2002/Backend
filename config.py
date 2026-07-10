import os


class Settings:
    PROJECT_NAME: str = "CTRL+SHIP Engine API"
    VERSION: str = "2.1.0"
    DB_FILE: str = "database.db"

    # Admin passcode is read from the environment if set, otherwise falls
    # back to this default. Change ADMIN_PASSCODE via environment variable
    # for anything beyond local dev — don't rely on the fallback in production.
    MASTER_PASSCODE: str = os.environ.get("ADMIN_PASSCODE") or "Tyagiboy@123"

    # Comma-separated list of allowed CORS origins. Defaults to permissive
    # local dev origins; set CORS_ORIGINS in production to your real domain.
    CORS_ORIGINS: list[str] = os.environ.get(
        "CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173"
    ).split(",")


settings = Settings()
