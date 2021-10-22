from django.db import models

# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    sport = models.ForeignKey(Sport(), on_delete=models.CASCADE, null=True)
    number_of_rounds = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Player(models.Model):
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=30)

    class Meta:
        unique_together = ['firstname', 'lastname']

    def __str__(self):
        return self.firstname+' '+self.lastname


class Participant(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    initial_rating = models.IntegerField(null=True)

    class Meta:
        unique_together = ['tournament', 'player', ]
        ordering = ['tournament', 'player', ]

    def __str__(self):
        return '{} ({})'.format(self.player, self.tournament)


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.IntegerField(null=False)
    player1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='player2')
    score1 = models.FloatField(null=True)
    score2 = models.FloatField(null=True)

    class Meta:
        unique_together = ['tournament', 'round', 'player1', 'player2', ]
        ordering = ['tournament', 'round', ]

    def __str__(self):
        return '{} {}-{} {}'.format(self.player1.firstname,
                                    self.score1, self.score2,
                                    self.player2.firstname,)
