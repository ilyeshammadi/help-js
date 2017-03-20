from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from .models import User
from .forms import LoginForm, RegisterForm


def login(request):

    form = LoginForm()
    context = {
        'form': form
    }

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Welcome back ' + str(username))
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.warning(request, 'This user does not exist')
            return render(request, 'users/login.html', context)
    else:
        return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        confirmed_password = request.POST['confirmed_password']

        if password != confirmed_password:
            messages.warning(request, "Wrong password !!")
            return render(request, 'users/register.html')

        user = User.objects.create(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Welcome to the blog ' + str(username))
            # Redirect to a success page.
            return redirect('home')
        else:
            # Return an 'invalid login' error message.
            messages.warning(request, 'This user does not exist')
            return render(request, 'users/register.html')
    else:
        form = RegisterForm()
        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'Bye Bye !!')
    return redirect('home')
