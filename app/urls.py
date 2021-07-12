from django.urls import path
from . import views

urlpatterns = [
    path('players/', views.players),
]
