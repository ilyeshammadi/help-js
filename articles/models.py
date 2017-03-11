from __future__ import unicode_literals

from django.urls import reverse

from users.models import User
from django.db import models

from taggit.managers import TaggableManager

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


class Message(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content


class Topic(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()

    tags = TaggableManager()

    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('articles:search_topics')





class Session(models.Model):
    topic = models.ForeignKey(Topic)
    senior = models.ForeignKey(User, related_name='senior', blank=True, null=True)
    junior = models.ForeignKey(User, related_name='junior')

    time = models.CharField(max_length=120)

    chat_room = models.ForeignKey(Message, blank=True, null=True)

    code = models.TextField(blank=True, null=True, default="# Hey coders !!")
    ended = models.BooleanField(default=False)


    def __str__(self):
        return str(self.topic.name)


