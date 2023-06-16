from django.db import models

# Create your models here.

class myModel(models.Model):
    Date = models.DateField(null=True)
    Competition = models.CharField(max_length=255, default="DEFAULT")
    Day = models.CharField(max_length=255, default="DEFAULT")
    Venue = models.CharField(max_length=255, default="DEFAULT")
    Result = models.CharField(max_length=255, default="DEFAULT")
    GF = models.IntegerField(default=-1)
    GA = models.IntegerField(default=-1)
    Opponent = models.CharField(max_length=255, default="DEFAULT")
    Possession = models.IntegerField(default=-1)
    Shots = models.IntegerField(default=-1)
    Shots_Target = models.IntegerField(default=-1)
    Yellow = models.IntegerField(default=-1)
    Red = models.IntegerField(default=-1)
    Fouls = models.IntegerField(default=-1)
    Offside = models.IntegerField(default=-1)
    Team = models.CharField(max_length=255, default="DEFAULT")

    def __str__(self):
        # date = self.
        return f'Date: {self.Date}, Competition: {self.Competition}, Day: {self.Day}, Venue: {self.Venue}, Result: {self.Result}, GF: {self.GF}, GA: {self.GA}, Opponent: {self.Opponent}, Possession: {self.Possession}, Shots: {self.Shots}, Shots on Target: {self.Shots_Target}, Yellow Cards: {self.Yellow}, Red Cards: {self.Red}, Fouls: {self.Fouls}, Offside: {self.Offside}, Team: {self.Team}'
