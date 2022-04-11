from django.contrib import admin
from django.urls import path, include
from dealerengine import views

urlpatterns = [
    path('', views.main, name='main'),
    path('1/', views.one, name='one'),
    path('2/', views.two, name='two'),
    path('3/', views.three, name='three'),

]
