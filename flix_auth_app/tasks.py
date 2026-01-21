from django.core.mail import send_mail
from django.conf import settings
from django_rq import job


@job
def send_activation_email(email, uid, token):
    subject = "Activate your VideoFlix account"
    activation_link = f"http://127.0.0.1:5500/pages/auth/activate.html?uid={uid}&token={token}"
    message = f"Moin, please click the link to activate your account: {activation_link}"

    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
