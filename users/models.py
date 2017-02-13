from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField(upload_to='users/', default='users/profile_image.png',blank=True)

    def __str__(self):
        return self.username
