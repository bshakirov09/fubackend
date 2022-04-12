from django.conf import settings
from sendgrid import Mail, SendGridAPIClient

from fitness.celery import app


@app.task
def send_email(email, subject, message):
    message = Mail(
        from_email=settings.SENDER_EMAIL,
        to_emails=[email],
        subject=subject,
        html_content=message,
    )
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    sg.send(message)
