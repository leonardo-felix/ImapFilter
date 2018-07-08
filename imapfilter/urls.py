from django.conf.urls import include, url
from django.views.generic import TemplateView
from .views import listar
from django.urls import path

urlpatterns = [
    path('listar', listar)
]
