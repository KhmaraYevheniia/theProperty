# Generated by Django 3.2.3 on 2021-06-04 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rega', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyObject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(verbose_name='latitude')),
                ('longitude', models.FloatField(verbose_name='longitude')),
                ('square', models.FloatField(verbose_name='square')),
                ('price', models.FloatField(verbose_name='price')),
                ('type', models.CharField(max_length=100, verbose_name='type')),
                ('address', models.CharField(max_length=300, verbose_name='address')),
                ('sold_status', models.BooleanField(default=False, verbose_name='sold_status')),
            ],
        ),
    ]
