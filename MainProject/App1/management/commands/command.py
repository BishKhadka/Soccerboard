from django.core.management.base import BaseCommand
from django.conf import settings
from App1.models import myModel
import csv
import os

class Command(BaseCommand):
    def handle(self, *args, **options):

        def deleteEntireModel():
            myModel.objects.all().delete()
            print('Message : All instances of myModel have been deleted.')

        deleteEntireModel()

        with open(os.path.join(settings.BASE_DIR, 'App1/PLData.csv'), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                myModel.objects.create(Date=row[0], Competition=row[1], 
                                       Day=row[2], Venue=row[3], Result=row[4],
                                       GF=row[5], GA=row[6], Opponent=row[7],
                                       Possession=row[8], Shots=row[9], Shots_Target=row[10],
                                       Yellow=row[11], Red=row[12], Fouls=row[13],
                                       Offside=row[14], Team=row[15],)