from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import mark_safe

class User(AbstractUser):
    image = models.ImageField(upload_to='users_avatars/%Y/%m/%d/', null=True, blank=True)
    is_verified_email = models.BooleanField(default=False)

    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(self.image.url))
    image_tag.short_description = 'Avatar'

