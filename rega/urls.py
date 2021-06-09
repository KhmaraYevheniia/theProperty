from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('registration', views.registration),
    path('sign_in', views.sign_in),
    path('sign_out', views.sign_out),
    path('create_object', views.create_object),
    path('create_contract', views.create_contract),
    path('contracts', views.contracts, name='contracts'),
    path('objects', views.objects, name='objects')
]
