from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('users', views.index, name='users'),
    path('registration', views.registration),
    path('sign_in', views.sign_in)
]
