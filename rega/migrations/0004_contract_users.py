# Generated by Django 3.2.3 on 2021-06-04 20:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rega', '0003_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
