# Generated by Django 4.0.3 on 2022-04-11 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealerengine', '0002_value_users'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
