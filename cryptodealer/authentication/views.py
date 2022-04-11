from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, "authentication/index.html")


def signup(request):
    if request.method == "POST":
        login = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        myuser = User.objects.create_user(login, email, password)

        myuser.save()

        messages.success(request, "Your account gas been created")

        return redirect("signin")

    return render(request, "authentication/signup.html")


def signin(request):
    return render(request, 'authentication/signin.html')


def signout(request):
    pass
