import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from cryptodealer import settings
from dealerengine.models import Users, Crypto, Value, Membership


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'HOST': '127.0.0.1',
        'NAME': 'database-1',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'USER': 'postgres',
        'PASSWORD': 'coderslab',
    }


@pytest.fixture
def user_data():
    print('user_data')
    return {'email': 'kaczka@a.pl', 'username': 'kaczkaa', 'password': 'dziwaczkaa'}


@pytest.fixture
def create_test_user(user_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    return test_user


@pytest.fixture
def authenticated_user(client, user_data):
    user_model = get_user_model()
    test_user = user_model.objects.create_user(**user_data)
    test_user.set_password(user_data.get('password'))
    test_user.save()
    client.login(**user_data)
    money = Users.objects.filter(pk=test_user.id).update(usd=99999999)
    users = User.objects.get(username="kaczkaa")
    members = Membership.objects.all()
    bitek = Crypto.objects.all()
    Value.objects.create(account=users, crypto=bitek[0], value=10)
    Value.objects.create(account=users, crypto=bitek[1], value=20)
    Value.objects.create(account=users, crypto=bitek[2], value=30)
    Value.objects.create(account=users, crypto=bitek[3], value=40)
    Value.objects.create(account=users, crypto=bitek[4], value=50)
    Users.objects.create(usd=99999999, account=users, member=members[1])
    return test_user
