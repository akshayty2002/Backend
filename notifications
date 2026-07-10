import logging
import httpx
from config import settings

logger = logging.getLogger("notifications")

RESEND_API_URL = "https://api.resend.com/emails"


def send_new_message_notification(message) -> None:
    """
    Sends an email alert when a new contact/inquiry message comes in.

    This is intentionally best-effort: if RESEND_API_KEY or NOTIFY_EMAIL
    isn't configured, or the Resend API call fails for any reason, this
    function logs the problem and returns quietly. A broken or unconfigured
    email integration must never prevent a message from being saved — the
    message is already committed to the database by the time this runs.
    """
    if not settings.RESEND_API_KEY or not settings.NOTIFY_EMAIL:
        logger.info("Email notifications not configured (RESEND_API_KEY/NOTIFY_EMAIL unset) — skipping.")
        return

    subject = f"New inquiry from {message.name}"
    body_lines = [
        f"Name: {message.name}",
        f"Email: {message.email}",
        f"Interested in: {message.interest}",
        f"Received: {message.timestamp}",
        "",
        "Message:",
        message.message,
        "",
        "---",
        "Reply directly to this sender's email, or view it in your admin dashboard.",
    ]
    text_body = "\n".join(body_lines)

    html_body = (
        f"<p><strong>Name:</strong> {message.name}<br>"
        f"<strong>Email:</strong> {message.email}<br>"
        f"<strong>Interested in:</strong> {message.interest}<br>"
        f"<strong>Received:</strong> {message.timestamp}</p>"
        f"<p><strong>Message:</strong><br>{message.message.replace(chr(10), '<br>')}</p>"
        f"<hr><p style='color:#666;font-size:13px;'>Reply directly to this sender's email, "
        f"or view it in your admin dashboard.</p>"
    )

    try:
        response = httpx.post(
            RESEND_API_URL,
            headers={
                "Authorization": f"Bearer {settings.RESEND_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "from": settings.FROM_EMAIL,
                "to": [settings.NOTIFY_EMAIL],
                "reply_to": message.email,
                "subject": subject,
                "text": text_body,
                "html": html_body,
            },
            timeout=10.0,
        )
        if response.status_code >= 400:
            logger.warning(
                "Resend notification failed (status %s): %s",
                response.status_code,
                response.text,
            )
    except Exception as exc:
        logger.warning("Resend notification failed: %s", exc)
