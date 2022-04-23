from django.contrib import admin
from django.urls import path, include
from dealerengine.views import CryptoWeb, MarketWeb, ProfileWeb, Dogecoin, Litecoin, Bitcoin, Tether, Ethereum, \
    HistoryWeb, BalanceWeb

urlpatterns = [
    path('', ProfileWeb.as_view(), name='profile_view'),
    path('crypto/', CryptoWeb.as_view(), name='crypto_view'),
    path('market/', MarketWeb.as_view(), name='market_view'),
    path('history/', HistoryWeb.as_view(), name='history_view'),
    path('crypto/1/', Bitcoin.as_view(), name='bitcoin_view'),
    path('crypto/2/', Litecoin.as_view(), name='litecoin_view'),
    path('crypto/3/', Dogecoin.as_view(), name='dogecoin_view'),
    path('crypto/4/', Tether.as_view(), name='tether_view'),
    path('crypto/5/', Ethereum.as_view(), name='ethereum_view'),
    path('balance/', BalanceWeb.as_view(), name='add_balance_view'),
]
