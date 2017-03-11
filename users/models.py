from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models


class Skill(models.Model):
    title = models.CharField(max_length=120)



# Create your models here.
class User(AbstractUser):
    profile_image = models.ImageField(upload_to='users/', default='users/profile_image.png',blank=True)
    skills = models.ForeignKey(Skill, blank=True, null=True)
    type = models.CharField(max_length=120, blank=True, null=True)

    github_link = models.CharField(max_length=250, blank=True, null=True)
    linkedin_link = models.CharField(max_length=250, blank=True, null=True)
    twitter_link = models.CharField(max_length=250, blank=True, null=True)
    website_link = models.CharField(max_length=250, blank=True, null=True)


    def __str__(self):
        return self.username



