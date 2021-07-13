from django.db import models

# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100, null=False)
    sport = models.ForeignKey(Sport(), on_delete=models.CASCADE)
    number_of_rounds = models.IntegerField(null=True)

    def __str__(self):
        return '{} ({})'.format(self.name, self.id)


class Player(models.Model):
    name = models.CharField(max_length=20, null=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    def __str__(self):
        return '{} ({})'.format(self.name, self.tournament)
