from django.db import models


class Crypto(models.Model):
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=90, decimal_places=2)


class Membership(models.Model):
    name = models.CharField(max_length=64)
    fees = models.IntegerField()

