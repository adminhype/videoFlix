from django.urls import path

from .views import activate_user, register_user

urlpatterns = [
    path('register/', register_user, name='register'),
    path('activate/<uidb64>/<token>/', activate_user, name='activate')
]
