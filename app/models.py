from django.db import models

# Create your models here.


class Sport(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=100, null=False)
    sport = models.ForeignKey(Sport(), on_delete=models.CASCADE, null=True)
    number_of_rounds = models.IntegerField(null=True)

    def __str__(self):
        return '{} [id={}]'.format(self.name, self.id)


class Player(models.Model):
    name = models.CharField(max_length=20, null=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)

    class Meta:
        unique_together = ['name', 'tournament']
        ordering = ['name']

    def __str__(self):
        return '{} ({})'.format(self.name, self.tournament)


class Match(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    round = models.IntegerField(null=False)
    player1 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='player2')
    points1 = models.FloatField(null=True)
    points2 = models.FloatField(null=True)

    def __str__(self):
        return '{} {}-{} {}'.format(self.player1.name[:10],
                                    int(self.points1) if int(
                                        self.points1) == self.points1 else self.points1,
                                    int(self.points2) if int(
                                        self.points2) == self.points2 else self.points2,
                                    self.player2.name[:10], )
