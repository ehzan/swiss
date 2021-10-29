from django.urls import path
from . import views

urlpatterns = [
    path('<int:tournamentId>/', views.scoreboard, name='scoreboard'),
    path('<int:tournamentId>/scoreboard/', views.scoreboard, name='scoreboard'),
    path('<int:tournamentId>/get-scoreboard/',
         views.get_scoreboard, name='get_scoreboard'),
    path('ratings/', views.ratings, name='ratings'),

    path('tournament/', views.tournament),
    path('<int:tournamentId>/tournament/', views.tournament, name='tournament'),
    path('<int:tournamentId>/save-tournament/',
         views.save_tournament, name='save_tournament'),

    path('<int:tournamentId>/round<int:round>/',
         views.round, name='round'),
    path('<int:tournamentId>/save-round<int:round>/',
         views.save_round, name='save_round'),

    # path('schedule/', views.schedule),
    path('preview/<int:tournamentId>-<int:round>/',
         views.preview, name='preview'),
    path('preview/', views.preview, name='preview1'),
]
