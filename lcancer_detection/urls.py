from django.contrib import admin
from django.urls import path
from .views import index
from django.views.generic import RedirectView

urlpatterns = [
    path('', index, name='index'),
    path('result', RedirectView.as_view(url="result"), name="result"),
]