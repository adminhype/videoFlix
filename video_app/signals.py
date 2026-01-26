import os
import shutil

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings

from .models import Video
from .tasks import convert_to_hls


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    if created and instance.video_file:
        convert_to_hls.delay(instance.id, instance.video_file.path)


@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, **kwargs):
    if instance.video_file and os.path.isfile(instance.video_file.path):
        os.remove(instance.video_file.path)

    hls_dir = os.path.join(settings.MEDIA_ROOT, 'hls', str(instance.id))
    if os.path.isdir(hls_dir):
        shutil.rmtree(hls_dir)
