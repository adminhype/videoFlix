from unfold.admin import ModelAdmin

from django.contrib import admin

from .models import Video


@admin.register(Video)
class VideoAdmin(ModelAdmin):
    list_display = [
        "title",
        "category",
        "created_at",
        "has_720p",
        "has_1080p"
    ]
    search_fields = ["title", "description"]
    list_filter = ["category", "created_at"]

    fieldsets = (
        (None, {"fields": ("title", "description", "category")}),
        ("Media", {"fields": ("video_file", "thumbnail")}),
        ("Conversion Status", {"fields": ("has_720p", "has_1080p")}),
    )
