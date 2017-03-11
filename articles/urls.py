from django.conf.urls import url, include
from django.contrib import admin

from .views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^article/(?P<id>\d+)$', detail, name='detail'),
    url(r'^chatroom/(?P<id>\d+)$', chatroom, name='chatroom'),
    url(r'^search$', search_topics, name='search_topics'),
    url(
        regex=r'^create/$',
        view=TopicCreateView.as_view(),
        name='create'
    ),
    url(
        r'^create-chatroom/(?P<topic_id>\d+)$',
        view=create_chatroom,
        name='create-chatroom'
    )
]
