from django.conf import settings


def set_token_cookies(response, access_token, refresh_token):
    cookie_params = {
        "httponly": True,
        "secure": not settings.DEBUG,
        "samesite": "Lax"
    }
    response.set_cookie(
        "access_token",
        access_token,
        max_age=15 * 60,
        **cookie_params
    )
    response.set_cookie(
        "refresh_token",
        refresh_token,
        max_age=24 * 60 * 60,
        **cookie_params
    )
    return response
