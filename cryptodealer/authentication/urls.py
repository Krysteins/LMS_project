from django.contrib import admin
from django.urls import path, include
from authentication import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register_view'),
    path('login', views.loginin, name='login_view'),
    path('signout', views.signout, name='signout'),
]
