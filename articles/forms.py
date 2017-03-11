from django import forms

from .models import Article, Topic


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'content', 'image')



class AddTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ('name', 'description', 'tags')