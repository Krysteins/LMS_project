from decimal import Decimal
from django.contrib.auth.models import User
from dealerengine.models import Users, Value, Membership
from django import urls
from django.contrib.auth import get_user_model
import pytest


# test with logged user and try open website
@pytest.mark.parametrize('param', [
    ('profile_view'),
    ('crypto_view'),
    ('market_view'),
    ('history_view'),
    ('bitcoin_view'),
    ('litecoin_view'),
    ('dogecoin_view'),
    ('tether_view'),
    ('ethereum_view'),
    ('add_balance_view'),
])
@pytest.mark.django_db
def test_render_views_with_login(client, authenticated_user, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    print(temp_url)
    assert resp.status_code == 200


# test with not logged user and try open website
@pytest.mark.parametrize('param', [
    ('profile_view'),
    ('crypto_view'),
    ('market_view'),
    ('history_view'),
    ('bitcoin_view'),
    ('litecoin_view'),
    ('dogecoin_view'),
    ('tether_view'),
    ('ethereum_view'),
    ('add_balance_view'),
])
def test_render_views(client, param):
    temp_url = urls.reverse(param)
    resp = client.get(temp_url)
    assert resp.status_code == 302


@pytest.mark.django_db
def test_memberships(client, authenticated_user):
    member_url = urls.reverse('market_view')
    members = Users.objects.get(account=authenticated_user)
    print(members.member)
    resp = client.post(member_url, {'buy2': True})
    members = Users.objects.get(account=authenticated_user)
    print(members.member)
    assert resp.status_code == 302


@pytest.mark.django_db
def test_add_balance(client, authenticated_user):
    balance_url = urls.reverse('add_balance_view')
    cash = Users.objects.get(account=authenticated_user)
    monej = 99999999.00
    assert cash.usd == monej
    resp = client.post(balance_url, {'cash': 10, 'buy': True})
    cash = Users.objects.get(account=authenticated_user)
    assert cash.usd == monej + 10


@pytest.mark.django_db
def test_add_balance_decimal(client, authenticated_user):
    balance_url = urls.reverse('add_balance_view')
    cash = Users.objects.get(account=authenticated_user)
    monej = 99999999.00
    assert cash.usd == monej
    resp = client.post(balance_url, {'cash': 10.11, 'buy': True})
    cash = Users.objects.get(account=authenticated_user)
    summary1 = Decimal(monej + 10.12)
    summary2 = Decimal(monej + 10.10)
    assert cash.usd < summary1
    assert cash.usd > summary2


################################################################################## cryptocurrency tests!
@pytest.mark.django_db
def test_crypto_bitcoin_add(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=1)
    money = Users.objects.get(account=authenticated_user)
    print(f'{money.usd} $')
    bitcoin_url = urls.reverse('bitcoin_view')
    data = {
        'take_price': 1,
        'buy': True
    }
    print(cryptocurrency.value)
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    money = Users.objects.get(account=authenticated_user)
    print(f'{money.usd} $')
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=1)
    print(cryptocurrency.value)


@pytest.mark.django_db
def test_crypto_bitcoin_minus(client, authenticated_user):
    user_model = get_user_model()
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=1)
    bitcoin_url = urls.reverse('bitcoin_view')
    data = {
        'take_price': 1,
        'sell': True
    }
    print(cryptocurrency.value)
    money = Users.objects.get(account=authenticated_user)
    print(f'{money.usd} $')
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=1)
    print(cryptocurrency.value)
    money = Users.objects.get(account=authenticated_user)
    print(f'{money.usd} $')


@pytest.mark.django_db
def test_crypto_litecoin_add(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=2)
    bitcoin_url = urls.reverse('litecoin_view')
    data = {
        'take_price': 5,
        'buy': True
    }
    print(cryptocurrency.value)
    money = Users.objects.get(account=authenticated_user)
    print(f'{money.usd} $')
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=2)
    print(cryptocurrency.value)
    money = Users.objects.get(account=authenticated_user)
    print(f'{money.usd} $')


@pytest.mark.django_db
def test_crypto_litecoin_minus(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=2)
    bitcoin_url = urls.reverse('litecoin_view')
    data = {
        'take_price': 5,
        'sell': True
    }
    print(cryptocurrency.value)
    money = Users.objects.get(account=authenticated_user)
    print(f'{money.usd} $')
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=2)
    print(cryptocurrency.value)
    money = Users.objects.get(account=authenticated_user)
    print(f'{money.usd} $')


@pytest.mark.django_db
def test_crypto_dogecoin_add(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=3)
    bitcoin_url = urls.reverse('dogecoin_view')
    data = {
        'take_price': 10,
        'buy': True
    }
    print(cryptocurrency.value)
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=3)
    print(cryptocurrency.value)


@pytest.mark.django_db
def test_crypto_dogecoin_minus(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=3)
    bitcoin_url = urls.reverse('dogecoin_view')
    data = {
        'take_price': 10,
        'sell': True
    }
    print(cryptocurrency.value)
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=3)
    print(cryptocurrency.value)


@pytest.mark.django_db
def test_crypto_dogecoin_add(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=4)
    bitcoin_url = urls.reverse('tether_view')
    data = {
        'take_price': 15,
        'buy': True
    }
    print(cryptocurrency.value)
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=4)
    print(cryptocurrency.value)


@pytest.mark.django_db
def test_crypto_dogecoin_minus(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=4)
    bitcoin_url = urls.reverse('tether_view')
    data = {
        'take_price': 15,
        'sell': True
    }
    print(cryptocurrency.value)
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=4)
    print(cryptocurrency.value)


@pytest.mark.django_db
def test_crypto_dogecoin_add(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=5)
    bitcoin_url = urls.reverse('ethereum_view')
    data = {
        'take_price': 20.3104,
        'buy': True
    }
    print(cryptocurrency.value)
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=5)
    assert cryptocurrency.value > 50
    print(cryptocurrency.value)


@pytest.mark.django_db
def test_crypto_dogecoin_minus(client, authenticated_user):
    users = User.objects.get(username="kaczkaa")
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=5)
    bitcoin_url = urls.reverse('ethereum_view')
    data = {
        'take_price': 20.3104,
        'sell': True
    }
    print(cryptocurrency.value)
    resp = client.post(bitcoin_url, data=data)
    assert resp.status_code == 302
    cryptocurrency = Value.objects.get(account=authenticated_user, crypto=5)
    assert cryptocurrency.value < 50
    print(cryptocurrency.value)
