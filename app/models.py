from django.db import models

# Create your models here.


class Game(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100, null=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    number_of_rounds = models.IntegerField()

    def __str__(self):
        return self.name+'-'+self.id


class Player(models.Model):
    name = models.CharField(max_length=20, null=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.name, self.tournament)
