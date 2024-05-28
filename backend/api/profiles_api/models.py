from uuid import uuid4

from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import os
from PIL import Image


def get_unique_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('profile_pics', filename)


def validate_image(image):
    max_size_kb = 5 * 1024 * 1024
    if image.size > max_size_kb:
        raise ValidationError(f"Image file too large ( > 5MB )")

    ext = os.path.splitext(image.name)[1]
    valid_extensions = ['.png', '.jpeg', '.jpg']
    if ext.lower() not in valid_extensions:
        raise ValidationError(f"Unsupported file extension: {ext}. Use: .png, .jpeg, .jpg")


class Profile(models.Model):

    FIRST_NAME_MAX_LENGTH = 30
    LATEST_NAME_MAX_LENGTH = 30
    CLIENT_NUMBER_MAX_LENGTH = 6
    PHONE_NUMBER_MAX_LENGTH = 15

    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='profile',
                                blank=False,
                                null=False)

    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH,
                                  blank=True,
                                  null=True)

    last_name = models.CharField(max_length=LATEST_NAME_MAX_LENGTH,
                                 blank=True,
                                 null=True)

    client_number = models.CharField(max_length=CLIENT_NUMBER_MAX_LENGTH)

    email = models.EmailField()

    phone_number = models.CharField(max_length=PHONE_NUMBER_MAX_LENGTH,
                                    blank=True,
                                    null=True)

    profile_picture = models.ImageField(upload_to=get_unique_filename,
                                        validators=[validate_image])

    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if self.profile_picture:
            super().save(*args, **kwargs)

            img = Image.open(self.profile_picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_picture.path)

        else:
            super().save(*args, **kwargs)