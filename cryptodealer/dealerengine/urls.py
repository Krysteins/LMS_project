from django.contrib import admin
from django.urls import path, include
from dealerengine.views import CryptoWeb, MarketWeb, ProfileWeb

urlpatterns = [
    path('', ProfileWeb.as_view(), name='profile_view'),
    path('crypto/', CryptoWeb.as_view(), name='crypto_view'),
    path('market/', MarketWeb.as_view(), name='market_view'),
    # path('3/', views.three, name='three'),

]
