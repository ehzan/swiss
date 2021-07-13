from django.shortcuts import render

# Create your views here.


def tournament(request):
    players_list = ['Radin', 'Shima', 'Ava', 'Iliya Z.', 'Iliya E.', ]
    context = {}
    # context={'tournament': 'Tavana', 'tournamentId': 14, 'game': 'Backgammon', 'number_of_rounds': 5, 'players_list': players_list}
    return render(request, 'tournament.html', context)


def schedule(request):
    print('=========')
    requestData = request.POST if request.method == 'POST' else (
        request.Get if request.method == 'Get' else None)
    context = {}
    if requestData:
        for item in requestData:
            context[item] = requestData[item]
    context['players_list'] = context['players_list'].replace(',', ', ')
    print(context)
    return render(request, 'schedule.html', context)
