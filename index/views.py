from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'pages/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'pizza/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
            except IntegrityError:
                return render(request, 'pizza/signupuser.html', {'form': UserCreationForm(), 'error': 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, 'pizza/signupuser.html', {'form': UserCreationForm(), 'error':'Password did not match'})
@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'pizza/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'pizza/loginuser.html', {'form': AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)


