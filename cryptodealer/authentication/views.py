from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from dealerengine.models import Users, Value, Crypto, Membership


# displaying the home page
def home(request):
    return render(request, "main_site.html")


# registering a new user, insertion basic data: login, email, password
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
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
        membership = Membership.objects.all()
        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        adduser = Users.objects.create(account=myuser, usd=10, member=membership[1])
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


# logging into the system, throwing an error message when it is committed
def loginin(request):
    if request.method == "POST":
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            current_user = request.user
            user_id = current_user.id
            users = Users.objects.filter(account=user_id)
            ##########
            crypto = Value.objects.filter(account=user_id).order_by('id')
            crypto_name = Crypto.objects.all()
            value = 1
            context = {
                'users': users,
                'crypto': crypto,
                'crypto_name': crypto_name
            }
            return render(request, "profile.html", context=context)
        else:
            messages.error(request, "Wrong login or password")
            return redirect('login_view')

    return render(request, 'authentication/login.html')


# logging out of the user
def signout(request):
    logout(request)
    return redirect('home')
