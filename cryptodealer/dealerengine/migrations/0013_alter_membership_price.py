# Generated by Django 4.0.3 on 2022-04-22 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealerengine', '0012_alter_users_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='price',
            field=models.IntegerField(default=1),
        ),
    ]
