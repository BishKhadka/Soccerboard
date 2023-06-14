from django.db import models

# Create your models here.

class myModel(models.Model):
    Date = models.CharField(max_length=255, default="DEFAULT")
    print(Date)
    Competition = models.CharField(max_length=255, default="DEFAULT")
    Day = models.CharField(max_length=255, default="DEFAULT")
    Venue = models.CharField(max_length=255, default="DEFAULT")
    Result = models.CharField(max_length=255, default="DEFAULT")
    GF = models.IntegerField(default=-1)
    GA = models.IntegerField(default=-1)
    Opponent = models.CharField(max_length=255, default="DEFAULT")
    Possession = models.DecimalField(max_digits=5, decimal_places=1, default=-1.0)
    Shots = models.DecimalField(max_digits=5, decimal_places=1, default=-1.0)
    Shots_Target = models.DecimalField(max_digits=5, decimal_places=1, default=-1.0)
    Yellow = models.DecimalField(max_digits=5, decimal_places=1, default=-1.0)
    Red = models.DecimalField(max_digits=5, decimal_places=1, default=-1.0)
    Fouls = models.DecimalField(max_digits=5, decimal_places=1, default=-1.0)
    Offside = models.DecimalField(max_digits=5, decimal_places=1, default=-1.0)
    Team = models.CharField(max_length=255, default="DEFAULT")

    def __str__(self):
        return f'Date: {self.Date}, Competition: {self.Competition}, Day: {self.Day}, Venue: {self.Venue}, Result: {self.Result}, GF: {self.GF}, GA: {self.GA}, Opponent: {self.Opponent}, Possession: {self.Possession}, Shots: {self.Shots}, Shots on Target: {self.Shots_Target}, Yellow Cards: {self.Yellow}, Red Cards: {self.Red}, Fouls: {self.Fouls}, Offside: {self.Offside}, Team: {self.Team}'
