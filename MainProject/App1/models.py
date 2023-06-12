from django.db import models

# Create your models here.

class myModel(models.Model):
    Date = models.CharField(max_length=255, default="DEFAULT")
    Time = models.CharField(max_length=255, default="DEFAULT")
    Competition = models.CharField(max_length=255, default="DEFAULT")
    Day = models.CharField(max_length=255, default="DEFAULT")
    Venue = models.CharField(max_length=255, default="DEFAULT")
    Result = models.CharField(max_length=255, default="DEFAULT")
    GF = models.CharField(max_length=255, default="DEFAULT")
    GA = models.CharField(max_length=255, default="DEFAULT")
    Opponent = models.CharField(max_length=255, default="DEFAULT")
    Possession = models.CharField(max_length=255, default="DEFAULT")
    Shots = models.CharField(max_length=255, default="DEFAULT")
    Shots_Target = models.CharField(max_length=255, default="DEFAULT")
    Yellow = models.CharField(max_length=255, default="DEFAULT")
    Red = models.CharField(max_length=255, default="DEFAULT")
    Fouls = models.CharField(max_length=255, default="DEFAULT")
    Offside = models.CharField(max_length=255, default="DEFAULT")
    Team = models.CharField(max_length=255, default="DEFAULT")

    def __str__(self):
        return f'Haha This is a test page for printing table'
        # return f'{self.Date},{self.Time},{self.Competition},{self.Day},{self.Venue},{self.Result},{self.GF},{self.GA},{self.Opponent},{self.Possession},{self.Shots},{self.Shots_Target},{self.Yellow},{self.Red},{self.Fouls},{self.Offside},{self.Team}'
