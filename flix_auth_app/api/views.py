from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from .serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    RegisterSerializer
)

from flix_auth_app.tasks import send_activation_email, send_password_reset_email

from .utils import set_token_cookies, clear_token_cookies
from .services import get_user_from_uid, generate_mail_context, blacklist_token


User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        mail_context = generate_mail_context(user)

        send_activation_email.delay(user.email, mail_context["uid"], mail_context["token"])

        return Response({
            "user": {"id": user.id, "email": user.email},
            "token": mail_context["token"]
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def activate_user(request, uidb64, token):
    user = get_user_from_uid(uidb64)
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Account successfully activated."}, status=status.HTTP_200_OK)
    return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            set_token_cookies(
                response,
                response.data.pop("access", None),
                response.data.pop("refresh", None)
            )
        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"detail": "Refresh token required."}, status=status.HTTP_400_BAD_REQUEST)

        blacklist_token(refresh_token)

        response = Response(
            {"detail": "Logout successful! All tokens will be deleted. Refresh token ist now invalid."},
            status=status.HTTP_200_OK
        )
        return clear_token_cookies(response)


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"detail": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        request.data["refresh"] = refresh_token

        try:
            response = super().post(request, *args, **kwargs)

            if response.status_code == status.HTTP_200_OK:
                access_token = response.data.get("access")
                set_token_cookies(response, access_token, refresh_token)
                response.data["detail"] = "Token refreshed"
            return response

        except (InvalidToken, TokenError):
            return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get("email")
    try:
        user = User.objects.get(email=request.data.get("email"))
        context_mail = generate_mail_context(user)
        send_password_reset_email.delay(email, context_mail["uid"], context_mail["token"])
    except User.DoesNotExist:
        pass

    return Response({"detail": "An email has been sent to reset your password."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    user = get_user_from_uid(uidb64)

    if not user or not default_token_generator.check_token(user, token):
        return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = PasswordResetConfirmSerializer(data=request.data)
    if serializer.is_valid():
        user.set_password(serializer.validated_data["new_password"])
        user.save()
        return Response({"detail": "Your Password has been successfully reset."}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
