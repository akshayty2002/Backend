from .auth import router as auth_router
from .listings import router as listings_router
from .messages import router as messages_router

# Expose the modules clearly to main.py
__all__ = ["auth", "listings", "messages"]
