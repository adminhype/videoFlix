from unfold.admin import ModelAdmin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = [
        "email",
        "username",
        "is_verified",
        "is_staff",
        "is_active",
        "date_joined"
    ]
    search_fields = ["email", "username"]
    list_filter = ["is_staff", "is_active", "is_verified"]

    ordering = ["email"]

    fieldsets = (
        (None, {
            "fields": ("email", "username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_verified",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password", "confirm_password"),
        }),
    )
