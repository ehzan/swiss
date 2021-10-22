from django.urls import path
from . import views

urlpatterns = [
    path('scoreboard/', views.scoreboard),
    path('tournament/', views.tournament),
    path('tournament/<int:tournamentId>/', views.tournament, name='tournament'),
    path('save-tournament/',
         views.save_tournament, name='save_tournament'),
    path('save-tournament/<int:tournamentId>/',
         views.save_tournament, name='save_tournament'),
    # path('schedule/', views.schedule),
    path('preview/<int:tournamentId>-<int:round>/',
         views.preview, name='preview'),
    path('preview/', views.preview, name='preview1'),
    path('round/<int:tournamentId>-<int:round>/',
         views.round, name='round'),
    path('save-round/<int:tournamentId>-<int:round>/',
         views.save_round, name='save_round'),
]
