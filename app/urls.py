from django.urls import path
from . import views

urlpatterns = [
    path('tournament/', views.tournament),
    path('schedule/', views.schedule),
]
