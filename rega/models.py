from django.db import models

class User(models.Model):
    name = models.CharField('name', max_length=100)
    email = models.CharField('email', max_length=100)
    password = models.CharField('password', max_length=100)
    type = models.CharField('type', max_length=100)

    def __str__(self):
        return self.name
