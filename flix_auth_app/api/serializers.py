from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """Handles user register, including password confirm and inactive account creation."""
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "confirmed_password"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def validate(self, data):
        if data["password"] != data["confirmed_password"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        username = validated_data["email"].split("@")[0]
        user = User.objects.create_user(
            username=username,
            email=validated_data["email"],
            password=validated_data["password"],
            is_active=False
        )
        return user


class LoginSerializer(TokenObtainPairSerializer):
    """Validates credentials and returns the JWT pair along with user details."""

    def validate(self, attrs):
        data = super().validate(attrs)

        data.update({
            "detail": "Login successful",
            "user": {
                "id": self.user.id,
                "email": self.user.email
            }
        })
        return data


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Validate the new password input during the reset process."""
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError({
                "new_password": "Passwords do not match."
            })
        return data
