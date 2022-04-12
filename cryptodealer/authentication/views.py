from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from dealerengine.models import Users, Value, Crypto


def home(request):
    return render(request, "main_site.html")


def register(request):
    if request.method == "POST":
        username = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if User.objects.filter(username=username):
            messages.error(request, "Login already exist!")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('home')
        if password != password2:
            messages.error(request, "Password didn't match!")

        myuser = User.objects.create_user(login, email, password)
        myuser.save()
        adduser = Users.objects.create(account=myuser, usd=10)
        adduser.save()
        coins = Crypto.objects.all()
        addcrypto1 = Value.objects.create(value=0, account=myuser, crypto=coins[0])
        addcrypto1.save()
        addcrypto2 = Value.objects.create(value=0, account=myuser, crypto=coins[1])
        addcrypto2.save()
        addcrypto3 = Value.objects.create(value=0, account=myuser, crypto=coins[2])
        addcrypto3.save()
        addcrypto4 = Value.objects.create(value=0, account=myuser, crypto=coins[3])
        addcrypto4.save()
        addcrypto5 = Value.objects.create(value=0, account=myuser, crypto=coins[4])
        addcrypto5.save()

        messages.success(request, "Your account has been created")
        messages.success(request, "Now you can login")

        return redirect("login_view")

    return render(request, "authentication/register.html")


def loginin(request):
    if request.method == "POST":
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            login_name = user.username
            return render(request, "profile.html", {'login_name': login_name})
        else:
            messages.error(request, "Wrong login or password")
            return redirect('home')

    return render(request, 'authentication/login.html')


def signout(request):
    logout(request)
    return redirect('home')
