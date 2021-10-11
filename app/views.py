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


def preview(request):
    print('==========preview==========')
    data = request.POST if request.method == 'POST' else (
        request.Get if request.method == 'Get' else None)
    print(data)
    try:
        theSport = models.Sport.objects.get(name=data['sport'])
    except:
        return HttpResponse('Somthing went wrong!')
    theTour, created = models.Tournament.objects.get_or_create(
        name=data['tournamentName'])
    theTour.sport = theSport
    theTour.number_of_rounds = int(data['number_of_rounds'])
    theTour.save()

    participants_ratings = data['participants_ratings'].split(
        ',') if data['participants_ratings'] else []
    participants = []
    rating = {}
    for pr in participants_ratings:
        id = pr.split(':')[0]
        r = pr.split(':')[1]
        participants.append(int(id))
        rating[int(id)] = int(r)

    models.Participant.objects.filter(
        tournament=theTour).exclude(player__id__in=participants).delete()
    for id in participants:
        participant, created = models.Participant.objects.get_or_create(
            player=models.Player.objects.get(id=id), tournament=theTour)
        participant.initial_rating = rating[id]
        participant.save()

    context = {'sport': theTour.sport.name, 'tournamentName': theTour.name,
               'number_of_rounds': theTour.number_of_rounds,
               'participants': models.Participant.objects.filter(tournament=theTour).order_by('-initial_rating')}
    print(context)
    return render(request, 'preview.html', context)
