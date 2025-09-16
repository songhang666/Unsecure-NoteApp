import logging
from django.core import mail

logger = logging.getLogger(__name__)

FROM = "seng406@unsecure.app"
APP_NAME = "Unsecure NoteApp"
FOOTER = "\n\n This is an automated message from Unsecure NoteApp. Please do not reply to this email."


def send_registration_code(to_email, code):
    """Send a registration code to the user's email.

    :param to_email: The email address to send the code to.
    :param code: The registration code to include in the email.
    """
    subject = APP_NAME + " - Your Registration Code"
    content = f"Thank you for registering! Your registration code is: {code}" + FOOTER
    send_email(to_email, subject, content)

def send_password_reset(to_email, reset_code):
    """Send a password reset link to the user's email.

    :param to_email: The email address to send the reset link to.
    :param reset_code: The code (OTP) for resetting the password.
    """
    subject = APP_NAME + " - Password Reset Request"
    content = f"To reset your password, please use the following code: {reset_code}" + FOOTER
    send_email(to_email, subject, content)

def send_email(to_email, subject, content):
    """Send an email with the specified subject and content.

    :param to_email: The email address to send the email to.
    :param subject: The subject of the email.
    :param content: The content of the email.
    """
    to_send = mail.EmailMessage(
        subject,
        content,
        FROM,
        [to_email]
    )
    to_send.send()
    logger.info("Email sent to %s with subject: %s", to_email, subject)
