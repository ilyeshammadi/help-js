from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import ArticleForm
from .models import Article


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
