from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Crypto(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=90, decimal_places=2)


class Membership(models.Model):
    name = models.CharField(max_length=64)
    fees = models.IntegerField()
    price = models.IntegerField(default=0)


class Users(models.Model):
    account = models.OneToOneField(User, on_delete=models.CASCADE)
    usd = models.DecimalField(max_digits=22, decimal_places=2, default=10.00)
    member = models.ForeignKey(Membership, on_delete=models.CASCADE, default=1)
    cryptocurrency = models.ManyToManyField('Crypto', through='Value')


class Value(models.Model):
    account = models.ForeignKey(Users, on_delete=models.CASCADE)
    crypto = models.ForeignKey(Crypto, on_delete=models.CASCADE, default=None)
    value = models.DecimalField(max_digits=100, decimal_places=8, default=0)


class History(models.Model):
    date_exchange = models.DateTimeField(auto_now_add=True)
    transaction = models.CharField(max_length=32)
    account = models.ManyToManyField(User)
    name_crypto = models.CharField(max_length=32, default="")
    value_crypto = models.DecimalField(max_digits=100, decimal_places=8, default=0)
    value_usd = models.DecimalField(max_digits=100, decimal_places=2, default=0)
