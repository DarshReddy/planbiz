# Generated by Django 3.0.5 on 2020-04-17 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurantapi', '0006_auto_20200417_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datematch',
            name='timeofvisit',
            field=models.TimeField(auto_now=True),
        ),
    ]
