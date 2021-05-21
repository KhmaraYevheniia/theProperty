from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('registration', views.registration),
    path('rega', views.index)
]
