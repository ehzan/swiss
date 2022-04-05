from django.shortcuts import render
from . import models
from django.db.models import Value, IntegerField, FloatField, CharField, F, Func, ExpressionWrapper, Max
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def scoreboard(request, tournamentId):
    print(tournamentId)
    theTour = models.Tournament.objects.get(id=tournamentId)
    context = {'tournament': theTour}
    return render(request, 'scoreboard.html', context=context)


# @csrf_exempt
def save_aunt(request, tournamentId=None):
    print('==========save_aunt==========')
    data = json.load(request)
    print(data)
    return HttpResponse('aunt!')


def get_scoreboard(request, tournamentId=None):
    print('======load-scoreboard=========')
    # return JsonResponse({'data': 'amghazi'})
    print(request.POST)
    print(json.load(request))
    table1 = table(tournamentId, models.Tournament.objects.get(
        id=tournamentId).number_of_rounds+1)
    print(table1)
    print(current_matches(tournamentId))
    # return JsonResponse(table1)
    return JsonResponse({'table': table1, 'matches': current_matches(tournamentId)})


def current_matches(tournamentId):
    round = models.Match.objects.filter(
        tournament__id=tournamentId).aggregate(max=Max('round'))['max']
    matches = models.Match.objects.filter(
        tournament__id=tournamentId, round=round)
    matches_list = [{'round': m.round, 'player1': m.player1.__str__(),
                     'player2': m.player2.__str__(), 'score1': m.score1, 'score2': m.score2}
                    for m in matches]
    return matches_list


def tournament(request, tournamentId=None):
    print('==========tournament==========')
    print(tournamentId)
    players_list = models.Player.objects.all().order_by('firstname', 'lastname')
    sports_list = models.Sport.objects.all()
    theTour = models.Tournament.objects.get(
        id=tournamentId) if tournamentId else None
    participants = models.Participant.objects.filter(
        tournament=theTour).order_by('-initial_rating')
    context = {'tournament': theTour, 'sports_list': sports_list,
               'players_list': players_list,
               'participants': participants, }
    print(context)
    return render(request, 'tournament.html', context)


def save_tournament(request, tournamentId=None):
    print('==========save-tournament==========')
    data = request.POST
    print(data)
    try:
        theSport = models.Sport.objects.get(name=data['sport'])
    except:
        return HttpResponse('Somthing went wrong!')
    if (tournamentId):
        theTour = models.Tournament.objects.get(id=tournamentId)
    else:
        try:
            theTour, created = models.Tournament.objects.get_or_create(
                name=data['tournamentName'])
        except:
            return HttpResponse('"{}" is unavailable.'.format(data['tournamentName']))
    theTour.name = data['tournamentName']
    theTour.sport = theSport
    theTour.number_of_rounds = int(data['number_of_rounds'])
    theTour.save()

    ratings = json.loads(data['participants_ratings'])
    models.Participant.objects.filter(
        tournament=theTour).exclude(player__id__in=ratings).delete()
    for id in ratings:
        participant, created = models.Participant.objects.get_or_create(
            player=models.Player.objects.get(id=id), tournament=theTour)
        participant.initial_rating = ratings[id]
        participant.save()

    return HttpResponseRedirect(reverse('tournament', args=(theTour.id,)),)


def preview(request, tournamentId=None, round=None):
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

    context = {'sport': theTour.sport.name,
               'tournamentId': theTour.id, 'tournamentName': theTour.name,
               'number_of_rounds': theTour.number_of_rounds,
               'participants': models.Participant.objects.filter(tournament=theTour).order_by('-initial_rating')}
    print(context)
    return render(request, 'preview.html', context)


def save_round(request, tournamentId=None, round=None):
    print('==========save_round==========')
    data = request.POST
    results = json.loads(data['results'])

    theTour = models.Tournament.objects.get(id=tournamentId)
    models.Match.objects.filter(tournament=theTour, round=round).delete()

    for result in results:
        plyr1 = models.Participant.objects.get(
            tournament=theTour, player__id=result['playerId1']).player
        plyr2 = models.Participant.objects.get(
            tournament=theTour, player__id=result['playerId2']).player

        if models.Match.objects.filter(tournament=theTour, player1=plyr1, player2=plyr2).exists() or \
                models.Match.objects.filter(tournament=theTour, player1=plyr2, player2=plyr1).exists():
            print('Duplicate Match!')
            return HttpResponse('Duplicate Match!')

        models.Match.objects.create(tournament=theTour, round=round,
                                    player1=plyr1, player2=plyr2,
                                    score1=result['score1'], score2=result['score2'])

    print(models.Match.objects.all())
    return HttpResponse('Data Saved!')


def points(won, drawn, lost, sport='Table Tennis'):
    return 2*won+1*lost


def tiebreak(Sa, Sb, Pa, Pb):
    tiebreak = Pb if Sa > Sb else 0.5*Sb if Sa == Sb else 0
    return tiebreak


def rating_change(Sa, Sb, Ra, Rb, K=60):
    if (Rb == 0 and Sa > Sb) or (Ra == 0 and Sa < Sb):
        return 0
    # K = 150
    S = 1 if Sa > Sb else (0 if Sa < Sb else 0.5)
    Ea = (10**(Ra/400))/(10**(Ra/400)+10**(Rb/400))
    return K*(S-Ea)


def table(tournamentId, round):
    print('==========table==========')

    participants = models.Participant.objects.filter(
        tournament__id=tournamentId)
    table = {p.player.id: {'playerId': p.player.id, 'playerName': p.player.__str__(),
                           'played': 0, 'points': 0, 'won': 0, 'drawn': 0, 'lost': 0, 'tiebreak': 0,
                           'initial_rating': p.initial_rating, 'rating': p.initial_rating, 'selected': False}
             for p in participants}

    for r in range(1, round+1):
        for m in models.Match.objects.filter(tournament__id=tournamentId, round=r):
            id1 = m.player1.id
            id2 = m.player2.id
            if m.score1 != None and m.score2 != None:
                table[id1]['played'] += 1
                table[id2]['played'] += 1
                if m.score1 > m.score2:
                    table[id1]['won'] += 1
                    table[id2]['lost'] += 1
                elif m.score1 < m.score2:
                    table[m.player1.id]['lost'] += 1
                    table[m.player2.id]['won'] += 1
                elif m.score1 == m.score2:
                    table[m.player1.id]['drawn'] += 1
                    table[m.player2.id]['drawn'] += 1
                c = rating_change(m.score1, m.score2,
                                  table[id1]['rating'], table[id2]['rating'])
                table[id1]['rating'] += c
                table[id2]['rating'] -= c
    for id in table:
        table[id]['points'] = points(
            table[id]['won'], table[id]['drawn'], table[id]['lost'])
    for r in range(1, round+1):
        for m in models.Match.objects.filter(tournament__id=tournamentId, round=r):
            id1 = m.player1.id
            id2 = m.player2.id
            if m.score1 != None and m.score2 != None:
                table[id1]['tiebreak'] += tiebreak(
                    m.score1, m.score2, table[id1]['points'], table[id2]['points'])
                table[id2]['tiebreak'] += tiebreak(
                    m.score2, m.score1, table[id2]['points'], table[id1]['points'])
    table = dict(sorted(table.items(),
                        key=lambda row: row[1]['playerName']))
    table = dict(sorted(table.items(),
                        key=lambda row: row[1]['points']*1000+row[1]['tiebreak']+row[1]['rating']/10000, reverse=True))
    return(table)


def round(request, tournamentId, round):
    print('==========round==========')
    theTour = models.Tournament.objects.get(id=tournamentId)
    results = models.Match.objects.filter(tournament=theTour, round=round)
    mytable = table(tournamentId, round-1)
    for match in results:
        mytable[match.player1.id]['selected'] = True
        mytable[match.player2.id]['selected'] = True
    context = {'tournament': theTour, 'round': round,
               'results': results, 'table': mytable, }
    return render(request, 'round.html', context)


def init_ratings(*tournamentIds):
    print('==========init_ratings==========')
    all_players = models.Participant.objects.filter(
        tournament__id__in=tournamentIds)
    players_list = dict(
        map(lambda p: (p.player.id, {'name': p.player.__str__(), 'played': 0, 'won': 0, 'lost': 0, 'rating': 900}), all_players))
    # players_list[0]['rating'] = 0
    for id in tournamentIds:
        print(id)
        if (not models.Tournament.objects.filter(id=id).exists()):
            print("{} doesn't exist".format(id))
            continue
        for p in models.Participant.objects.filter(tournament__id=id):
            p.initial_rating = players_list[p.player.id]['rating'] + 100\
                if p.player.firstname != 'Bye' else 0
            p.save()
        t1 = table(id, models.Tournament.objects.get(id=id).number_of_rounds+1)
        for row in t1.items():
            players_list[row[0]]['rating'] = row[1]['rating']
            players_list[row[0]]['played'] += row[1]['played']
            players_list[row[0]]['won'] += row[1]['won']
            players_list[row[0]]['lost'] += row[1]['lost']

    players_list = dict(sorted(players_list.items(),
                        key=lambda row: row[1]['rating'], reverse=True))
    return players_list


def ratings(request, tournamentIds=None):
    players_list = init_ratings(
        101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112)
    for player in players_list.items():
        player[1]['winPct'] = player[1]['won'] / \
            player[1]['played']*100 if player[1]['played'] else 0
    print(players_list)
    # players_list = models.Player.objects.all().order_by('firstname', 'lastname')
    context = {'players_list': players_list}
    return render(request, 'ratings.html', context=context)
