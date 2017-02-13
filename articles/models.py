from __future__ import unicode_literals

from users.models import User
from django.db import models

# Create your models here.
class Article(models.Model):
    user = models.ForeignKey(User)

    title = models.CharField(max_length=120)
    content = models.TextField(blank=True)

    image = models.ImageField(upload_to='images/')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'created'

    def __str__(self):
        return self.title