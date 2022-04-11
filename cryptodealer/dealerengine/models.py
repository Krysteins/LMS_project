from django.contrib.auth.models import User
from django.db import models


class Crypto(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=90, decimal_places=2)


class Membership(models.Model):
    name = models.CharField(max_length=64)
    fees = models.IntegerField()


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    usd = models.DecimalField(max_digits=12, decimal_places=2)
