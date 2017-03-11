from django.contrib import admin

# Register your models here.
from .models import Article, Session, Message, Topic

admin.site.register(Article)
admin.site.register(Session)
admin.site.register(Message)
admin.site.register(Topic)