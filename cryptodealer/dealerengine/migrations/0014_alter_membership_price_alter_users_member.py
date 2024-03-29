# Generated by Django 4.0.3 on 2022-04-22 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dealerengine', '0013_alter_membership_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='users',
            name='member',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dealerengine.membership'),
        ),
    ]
