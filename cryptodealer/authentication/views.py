from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, "main_site.html")


def signup(request):
    if request.method == "POST":
        username = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username):
            messages.error(request,"Login already exist!")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')
        if password != password2:
            messages.error(request, "Password didn't match!")

        myuser = User.objects.create_user(login, email, password)
        myuser.save()

        messages.success(request, "Your account gas been created")

        return redirect("signin")

    return render(request, "authentication/signup.html")


def loginin(request):
    if request.method == "POST":
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            login_name = user.username
            return render(request, "authentication/index.html", {'login_name': login_name})
        else:
            messages.error(request, "Wrong login or password")
            return redirect('home')

    return render(request, 'login.html')


def signout(request):
    logout(request)
    return redirect('home')
