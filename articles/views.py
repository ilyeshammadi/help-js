from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView

from .forms import ArticleForm, AddTopicForm
from .models import Article, Session, Topic


def home(request):
    return render(request, 'home.html')

# Create your views here.
def index(request):
    articles = Article.objects.all().order_by('-created')
    return render(request, 'articles/index.html', {'articles': articles})

def detail(request, id):
    article = get_object_or_404(Article, pk=id)
    return render(request, 'articles/detail.html', {'article' : article})


@login_required
def create(request):
    if request.method == 'POST':
        # Request the POST and FILES data
        # POST: title, content
        # FILES: image
        form = ArticleForm(request.POST, request.FILES)

        # If form is valid save the data
        if form.is_valid():

            # Get the data from the form without saving
            article = form.save(commit=False)

            # Assing the article to the logged in user
            article.user = request.user

            # Save the data
            article.save()

            # Show sucess message
            messages.success(request, "Artcile Created !!")

            # Redirect the user to home
            return redirect('articles:index')

        # If the form is not valid show an error message
        else:
            messages.error(request, "Error when creating the article :(")

    else:
        form = ArticleForm()

    context = {
        'form': form
    }

    return render(request, 'articles/create.html', context)


@login_required
def update(request, id):
    # Get the article to update
    article = get_object_or_404(Article, pk=id)

    # Check if the logged in user
    # is the owner of the article
    if article.user != request.user:
        messages.warning(request, "You're not the owner of this item")
        return redirect('articles:index')

    if request.method == 'POST':
        # Request the POST and FILES data
        # POST: title, content
        # FILES: image
        form = ArticleForm(request.POST, request.FILES, instance=article)

        # If form is valid save the data
        if form.is_valid():

            # Get the data from the form without saving
            form.save()

            # Show sucess message
            messages.success(request, "Artcile Updated !!")

            # Redirect the user to home
            return redirect('articles:index')

        # If the form is not valid show an error message
        else:
            messages.error(request, "Error when creating the article :(")

    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article
    }

    return render(request, 'articles/update.html', context)


@login_required
def delete(request, id):
    article = get_object_or_404(Article, pk=id)

    # Check if the logged in user
    # is the owner of the article
    if article.user != request.user:
        messages.warning(request, "You're not the owner of this item")
        return redirect('articles:index')

    article.delete()
    messages.warning(request, "Article deleted")
    return redirect('articles:index')

@login_required
def create_chatroom(request, topic_id):
    """Create a Chatroom using the Topic ID"""
    topic = get_object_or_404(Topic, pk=topic_id)

    session = Session()
    session.topic = topic
    session.junior = request.user
    session.save()

    return redirect('articles:chatroom', id=session.id)


@login_required
def chatroom(request, id):
    # Get the session from the database
    session = get_object_or_404(Session, pk=id)

    if session.ended:
        return redirect('articles:index')

    context = {
        'session' : session
    }
    return render(request, 'chatroom.html', context)


class TopicCreateView(CreateView):
    model = Topic
    form_class = AddTopicForm
    template_name = 'topic_add.html'


def search_topics(request):
    topics = Topic.objects.all()
    search = None

    if request.method == 'POST':
        search = request.POST.get('search')

    if search:
        terms = search.split(',')

        print("---------------- Terms ----------------")
        print(terms)

        q = Q()

        # Go through each term
        for term in terms:
            q |= Q(name__contains=term)
            q |= Q(description__contains=term)
            # q |= Q(tags__name__contains=term)

        topics = topics.filter(q).distinct()


    context = {
        'topics' : topics
    }


    return render(request, 'search.html', context)


def session_ended(request, id):
    print(id)
    session = get_object_or_404(Session, pk=id)
    session.ended = True
    print(session)
    session.save()
    return JsonResponse({'message' : 'session deleted'})


