from django.contrib import admin
from .models import User, PropertyObject, Contract

admin.site.register(User)
admin.site.register(PropertyObject)
admin.site.register(Contract)
