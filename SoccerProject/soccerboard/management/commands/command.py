from django.core.management.base import BaseCommand
from django.conf import settings
from soccerboard.models import TableModel
import csv
import os

class Command(BaseCommand):

    '''
    Custom management command to replace instances of the model.
    '''

    def handle(self, *args, **options):
        '''
        Replaces and populates the model instances with the data from the csv file.
        '''

        def deleteEntireModel():
            TableModel.objects.all().delete()

        deleteEntireModel()

        with open(os.path.join(settings.BASE_DIR, 'soccerboard/PLData.csv'), 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)
            for row in csv_reader:
                TableModel.objects.create(Date=row[0], Competition=row[1], 
                                       Day=row[2], Venue=row[3], Result=row[4],
                                       GF=row[5], GA=row[6], Opponent=row[7],
                                       Possession=row[8], Shots=row[9], Shots_Target=row[10],
                                       Yellow=row[11], Red=row[12], Fouls=row[13],
                                       Offside=row[14], Team=row[15],)
        print('Message : All instances of the model have been replaced with new data.')