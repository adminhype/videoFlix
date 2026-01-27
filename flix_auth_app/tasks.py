from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django_rq import job
from django.utils.html import strip_tags
from django.template.loader import render_to_string


@job
def send_activation_email(email, uid, token):
    """Sends an email containing the account activation link to the user."""
    subject = "Confirm your email"
    activation_link = f"http://127.0.0.1:5500/pages/auth/activate.html?uid={uid}&token={token}"
    context = {
        "link": activation_link,
        "username": email.split("@")[0]
    }
    html_content = render_to_string("emails/activation_email.html", context)
    text_content = strip_tags(html_content)

    email_msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()


@job
def send_password_reset_email(email, uid, token):
    """Sends an email containing the password reset link to the user."""
    subject = "Reset your Password"
    reset_link = f"http://127.0.0.1:5500/pages/auth/confirm_password.html?uid={uid}&token={token}"
    context = {
        "link": reset_link,
    }
    html_content = render_to_string("emails/password_reset_email.html", context)
    text_content = strip_tags(html_content)

    email_msg = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email_msg.attach_alternative(html_content, "text/html")
    email_msg.send()
