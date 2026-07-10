from fastapi import APIRouter, Header, HTTPException
from schemas import AuthRequest
from config import settings

# Explicitly initialize and export the auth APIRouter
router = APIRouter(prefix="/api/auth", tags=["Admin Portal Auth Gate"])


def verify_admin_token(authorization: str = Header(None), x_admin_passcode: str = Header(None)):
    """
    Protection dependency middleware check, injected across state-modifying
    endpoints to prevent malicious updates.

    Accepts either:
      - Authorization: Bearer <passcode>
      - X-Admin-Passcode: <passcode>
    This is the single place the passcode is validated; every protected
    route (listings write/update/delete, messages read) depends on this.
    """
    token = None
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ", 1)[1]
    elif x_admin_passcode:
        token = x_admin_passcode

    if token != settings.MASTER_PASSCODE:
        raise HTTPException(status_code=403, detail="Unauthorized system access attempt.")
    return token


@router.post("")
def check_passcode_session(payload: AuthRequest):
    """
    Validates the admin passcode sent from the frontend interface dashboard.
    """
    if payload.passcode == settings.MASTER_PASSCODE:
        return {"authenticated": True}
    raise HTTPException(status_code=401, detail="Invalid administrator token keys entered.")
