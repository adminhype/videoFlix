from django.conf import settings


def set_token_cookies(response, access_token, refresh_token):
    """Sets HTTP only cookies for access and refresh tokens."""
    cookie_params = {
        "httponly": True,
        "secure": not settings.DEBUG,
        "samesite": "Lax"
    }
    if access_token:
        response.set_cookie("access_token", access_token, max_age=15 * 60, **cookie_params)
    if refresh_token:
        response.set_cookie("refresh_token", refresh_token, max_age=24 * 60 * 60, **cookie_params)
    return response


def clear_token_cookies(response):
    """Removes auth cookies cookies from response."""
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response
