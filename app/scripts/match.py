from app import models
import re


def match(tour):
    print(repr(tour))


def run(*args):
    tourName = args[0] if len(args) > 0 else 'Najdorf Memorial 2021'
    with open('./Najdorf Memorial 2021/Resaults.txt', 'r', encoding='UTF-8') as f:
        resaults = f.read()
        resaults = re.split('^\d{2}\n|\n\d{2}\n', resaults)
        resaults.pop(0)
        resaults.reverse()
        resaults = [round.split('\n') for round in resaults]
    for round in resaults:
        for row in range(len(round)):
            round[row] = round[row].split('\t')
            round[row].pop(0)
            round[row].append(float(round[row][2][2])
                              if round[row][2][2].isdigit() else 0.5)
            round[row][2] = float(
                round[row][2][0]) if round[row][2][0].isdigit() else 0.5

        # resaults = map(lambda row: row.split('\n'), resaults)

    print(*resaults[1], sep='\n')
    tour = models.Tournament.objects.get(name=tourName)
    for row in resaults[1]:
        p1 = models.Player.objects.get(tournament=tour, name=row[0])
        p2 = models.Player.objects.get(tournament=tour, name=row[1])
        models.Match.objects.create(
            tournament=tour, round=2, player1=p1, player2=p2, points1=row[2], points2=row[3])

    # for name in names:
    #     models.Player.objects.create(name=name, tournament=tour, points=0)

    # match(tour)
