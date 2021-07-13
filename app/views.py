from django.shortcuts import render
from . import models
from django.http import HttpResponse

# Create your views here.


def tournament(request):
    players_list = ['Radin', 'Shima', 'Ava', 'Iliya Z.', 'Iliya E.', ]
    context = {}
    # context={'tournament': 'Tavana', 'tournamentId': 14, 'game': 'Backgammon', 'number_of_rounds': 5, 'players_list': players_list}
    return render(request, 'tournament.html', context)


def schedule(request):
    print('=========')
    data = request.POST if request.method == 'POST' else (
        request.Get if request.method == 'Get' else None)
    # for item in data:
    #     print(item, data[item])
    try:
        mySport = models.Sport.objects.get(name=data['game'])
    except:
        return HttpResponse('Somthing went wrong!')

    tourId = int(data['tournamentId']) if data['tournamentId'] else None
    myTour, created = models.Tournament.objects.get_or_create(
        id=tourId, sport=mySport)
    myTour.name = data['tournamentName']
    if (data['number_of_rounds']):
        myTour.number_of_rounds = int(data['number_of_rounds'])
    myTour.save()
    print(myTour.__dict__)
    # context['players_list'] = context['players_list'].replace(',', ', ')
    # print(context)
    return render(request, 'schedule.html', myTour.__dict__)
