from django.shortcuts import render
from . import models
from django.http import HttpResponse
# from django.views.decorators import csrf

# Create your views here.


def match(tour):
    players = models.Player.objects.filter(tournament=tour)
    if len(players) == 0:
        return None
    else:
        return None


def tournament(request):
    print('==========tournament==========')

    players_list = models.Player.objects.all().order_by('firstname', 'lastname')
    context = {}
    data = request.POST if request.method == 'POST' else (
        request.Get if request.method == 'Get' else {})
    for item in data:
        context[item] = data[item]
    print(context)
    context = {'tournament': 'Tavana', 'tournamentId': 14,
               'game': 'Backgammon', 'number_of_rounds': 5,
               'sports_list': ['Table Tennis', 'Chess', 'Backgammon', 'Volleyball'],
               'players_list': players_list
               }
    return render(request, 'tournament.html', context)


def schedule(request):
    print('==========schedule==========')
    data = request.POST if request.method == 'POST' else (
        request.Get if request.method == 'Get' else None)
    for item in data:
        print(item, data[item])
    try:
        theSport = models.Sport.objects.get(name=data['sport'])
    except:
        return HttpResponse('Somthing went wrong!')
    tourId = int(data['tournamentId']) if data['tournamentId'] else None
    theTour, created = models.Tournament.objects.get_or_create(
        id=tourId)
    theTour.name = data['tournamentName']
    theTour.sport = theSport
    if (data['number_of_rounds']):
        theTour.number_of_rounds = int(data['number_of_rounds'])
    theTour.save()
    players_list = data['players_list'].split(
        ',') if data['players_list'] else []
    models.Player.objects.filter(tournament=theTour).delete()
    for player in players_list:
        models.Player.objects.create(name=player, tournament=theTour)
    context = theTour.__dict__
    thePlayers = models.Player.objects.filter(
        tournament=theTour).values_list('name', flat=True)
    context['players_list'] = ', '.join(list(thePlayers))
    context['sport'] = theTour.sport.name
    context['tournamentId'] = theTour.id
    context['tournamentName'] = theTour.name
    print(context)

    # context['players_list'] = context['players_list'].replace(',', ', ')
    # print(context)
    return render(request, 'schedule.html', context)
