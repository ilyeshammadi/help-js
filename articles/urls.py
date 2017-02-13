from django.conf.urls import url, include
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^article/(?P<id>\d+)$', detail, name='detail'),
    url(r'^create$', create, name='create'),
    url(r'^update/(?P<id>\d+)$', update, name='update'),
    url(r'^delete/(?P<id>\d+)$', delete, name='delete'),
]
