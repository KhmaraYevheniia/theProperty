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
