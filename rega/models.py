from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class TypeUsers(models.TextChoices):
    ADMIN = 'admin', _('Администратор')
    MANAGER = 'manager', _('Менеджер')
    CHAIR = 'chair', _('Руководитель')

class User(AbstractUser):
    username = models.CharField('username', max_length=100, unique=True)
    name = models.CharField('username', max_length=100, default='name')
    email = models.CharField('email', max_length=100, unique=True)
    password = models.CharField('password', max_length=100)
    type = models.CharField(
        max_length=10,
        choices=TypeUsers.choices,
        default=TypeUsers.MANAGER,
    )

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def full_name(self):
        return self.first_name +' '+self.last_name

class PropertyObject(models.Model):
    latitude = models.FloatField('latitude')
    longitude = models.FloatField('longitude')
    square = models.FloatField('square')
    price = models.FloatField('price')
    type = models.CharField('type', max_length=100)
    address = models.CharField('address', max_length=300)
    sold_status = models.BooleanField('sold_status', default=False)

class Contract(models.Model):
    property_object = models.ForeignKey(PropertyObject, on_delete=models.CASCADE)
    sale_date = models.DateField()
    seller_name = models.CharField(max_length=100)
