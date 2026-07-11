import os


class Settings:
    PROJECT_NAME: str = "CTRL+SHIP Engine API"
    VERSION: str = "2.1.0"
    DB_FILE: str = "database.db"

    # Postgres connection string. Render auto-sets this when you attach a
    # Postgres database to this service (Environment tab will show it as
    # linked, or you can copy the "Internal Database URL" manually).
    # If unset, falls back to local SQLite (see database.py) — fine for
    # local dev, but NOT durable on Render's free tier (data resets on
    # every restart/sleep-wake cycle).
    DATABASE_URL: str = os.environ.get("DATABASE_URL", "")

    # Admin passcode is read from the environment if set, otherwise falls
    # back to this default. Change ADMIN_PASSCODE via environment variable
    # for anything beyond local dev — don't rely on the fallback in production.
    MASTER_PASSCODE: str = os.environ.get("ADMIN_PASSCODE") or "Tyagiboy@123"

    # Comma-separated list of allowed CORS origins. Defaults cover common
    # local Vite dev ports (5173 is default, but Vite auto-increments if
    # that port is busy).
    #
    # IMPORTANT: In production (e.g. backend on Render, frontend on Netlify),
    # you MUST set CORS_ORIGINS to your actual Netlify URL, e.g.:
    #   CORS_ORIGINS=https://your-site-name.netlify.app
    # Without this, the browser will block every request from your deployed
    # frontend with a CORS error (which often just looks like "Failed to
    # fetch" with no further detail).
    _cors_env = os.environ.get("CORS_ORIGINS")
    CORS_ORIGINS: list[str] = (
        _cors_env.split(",")
        if _cors_env
        else [
            f"http://{host}:{port}"
            for host in ("localhost", "127.0.0.1")
            for port in (5173, 5174, 5175, 4173)
        ]
    )

    # Email notifications (via Resend, https://resend.com — free tier,
    # no credit card required). Optional: if RESEND_API_KEY isn't set,
    # notification emails are silently skipped and the site keeps working
    # normally — message submissions still save to the database either way.
    #
    # Setup:
    #   1. Sign up at resend.com and create an API key.
    #   2. Set RESEND_API_KEY on your backend host (e.g. Render).
    #   3. Set NOTIFY_EMAIL to the address that should receive alerts.
    #   4. FROM_EMAIL must be a domain you've verified with Resend, OR use
    #      the sandbox default "onboarding@resend.dev" for testing (only
    #      delivers to the email you signed up with, on the free tier,
    #      until you verify your own domain).
    RESEND_API_KEY: str = os.environ.get("RESEND_API_KEY", "")
    NOTIFY_EMAIL: str = os.environ.get("NOTIFY_EMAIL", "")
    FROM_EMAIL: str = os.environ.get("FROM_EMAIL", "onboarding@resend.dev")


settings = Settings()

if not os.environ.get("CORS_ORIGINS"):
    print("\n" + "=" * 60)
    print("⚠️  CORS_ORIGINS not set — only localhost dev origins are allowed.")
    print("   If your frontend is deployed (e.g. on Netlify), set:")
    print("   CORS_ORIGINS=https://your-site-name.netlify.app")
    print("   on your backend host (e.g. Render's environment variables),")
    print("   or every request from that frontend will be blocked.")
    print("=" * 60 + "\n")
