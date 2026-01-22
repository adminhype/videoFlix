from django.urls import path

from .views import (
    CustomTokenRefreshView,
    LoginView,
    LogoutView,
    activate_user,
    register_user,
    password_reset_confirm,
    password_reset_request,
)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', password_reset_request, name='password_reset_request'),
    path('password_confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]
