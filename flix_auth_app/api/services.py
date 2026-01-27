from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

User = get_user_model()


def get_user_from_uid(uidb64):
    """Retrieves the user instance corresponding to the base64 encoded UID."""
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return None


def generate_mail_context(user):
    """Generates the UID and token required for email verification or password reset links."""
    return {
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user)
    }


def blacklist_token(refresh_token):
    """Invalidates the given refresh token by adding it to the blacklist."""
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
        return True
    except Exception:
        return False
