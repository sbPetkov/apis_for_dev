import os
from uuid import uuid4

from django.db import models


def get_unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"advice_{uuid4().hex}.{ext}"
    return os.path.join('advices_img', filename)


class Advice(models.Model):
    title = models.CharField(max_length=255)
    background_image = models.ImageField(upload_to=get_unique_filename)
    content = models.TextField()
    position = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['position']
