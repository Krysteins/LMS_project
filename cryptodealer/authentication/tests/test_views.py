import pytest
from django import urls
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from dealerengine import models, views
from django.urls import reverse
from django.test import Client
from authentication import views
#
#
# @pytest.mark.parametrize('param', [
#     ('home'),
#     ('register_view'),
#     ('login_view')
# ])
# def test_render_views(client, param):
#     temp_url = urls.reverse(param)
#     resp = client.get(temp_url)
#     assert resp.status_code == 200
#
#
# @pytest.mark.django_db
# def test_user_signup(client, user_data):
#     user_model = get_user_model()
#     register_urls = urls.reverse('register_view')
#     print(user_model.objects.all())
#     print(user_model.objects.count())
#     resp = client.post(register_urls, user_data)
#     print(user_model.objects.all())
#     print(user_model.objects.count())
#     assert resp.status_code == 302
#
#
#
# @pytest.mark.django_db
# def test_user_login(client, create_test_user, user_data):
#     user_model = get_user_model()
#     print(user_model.objects.count())
#     login_url = urls.reverse('login_view')
#     resp = client.post(login_url, data=user_data)
#     assert resp.status_code == 302
#     assert resp.url == urls.reverse('login_view')
#

#
#
# @pytest.mark.django_db
# def test_user_logout(client, authenticated_user):
#     logout_url = urls.reverse('signout')
#     resp = client.get(logout_url)
#     assert resp.status_code == 302
#     assert resp.url == urls.reverse('home')
#
#
# def test_new_user(django_user_model):
#     user_model = get_user_model()
#     print(user_model.objects.count())
#     new_account = django_user_model.objects.create(username="username1", password="password1")
#     print(user_model.objects.count())
#     new_account.save()
#     print(new_account)
#
#
# def test_an_admin_view(admin_client):
#     response = admin_client.get('/admin/')
#     assert response.status_code == 200
