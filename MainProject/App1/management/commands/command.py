from django.core.management.base import BaseCommand
from django.conf import settings
from App1.models import myModel
import csv 
import os

class Command(BaseCommand):
    def handle(self, *args, **options):
                # with open(os.path.join(settings.BASE_DIR, 'MainProject', 'App1', 'test.csv'), 'r') as csv_file:

        with open(os.path.join(settings.BASE_DIR, 'App1/PLData.csv'), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                myModel.objects.create(Date=row[0], Time=row[1], Competition=row[2], 
                                       Day=row[3], Venue=row[4], Result=row[5],
                                       GF=row[6], GA=row[7], Opponent=row[8],
                                       Possession=row[9], Shots=row[10], Shots_Target=row[11],
                                       Yellow=row[12], Red=row[13], Fouls=row[14],
                                       Offside=row[15], Team=row[16],)

mytable_elements = myModel.objects.all()
for element in mytable_elements:
    print(element.Competition, element.Team)
