from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Video(models.Model):
    class VideoCategory(models.TextChoices):
        DRAMA = "Drama", _("Drama")
        COMEDY = "comedy", _("Comedy")
        DOCUMENTARY = "documentary", _("Documentary")
        ACTION = "Action", _("Action")
        HORROR = "Horror", _("Horror")
        SCI_FI = "Sci-Fi", _("Sci-Fi")
        ROMANCE = "romance", _("Romance")

    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=112)
    description = models.TextField(blank=True, null=True)
    video_file = models.FileField(
        upload_to="videos/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["mp4", "avi", "mov", "mkv"])]
    )
    thumbnail = models.ImageField(upload_to="thumbnails/", blank=True, null=True)
    category = models.CharField(
        max_length=55,
        choices=VideoCategory.choices,
        default=VideoCategory.DRAMA
    )
    has_720p = models.BooleanField(default=False)
    has_1080p = models.BooleanField(default=False)

    def __str__(self):
        return self.title
