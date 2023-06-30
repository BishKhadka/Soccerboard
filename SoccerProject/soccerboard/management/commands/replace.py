from django.core.management.base import BaseCommand
from soccerboard.models import TableModel
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import concurrent.futures
import time
import threading
import requests
from datetime import datetime
from django.utils import timezone

class AllLeagueData(object):
    def __init__(self):
        '''
        Initialize the AllLeagueData object.
        '''
        self.url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        self.session = requests.Session()

    def get_url(self):
        '''
        Retrieve the URL for the Premier League statistics page.
        '''
        return self.url

    def all_club_links(self, url):
        '''
        Retrieve links to all club data pages from the given URL.
        '''
        try:
            response = self.session.get(url)
            response.raise_for_status() 
            soup = BeautifulSoup(response.text, "html.parser")
            team_table = soup.select("table.stats_table")[0]
            team_links = team_table.find_all("a")
            team_links = [l.get("href") for l in team_links if l.get("href")]
            team_links = [l for l in team_links if "/squads/" in l]
            team_links = [f"https://fbref.com{l}" for l in team_links]
            return team_links
        except requests.exceptions.RequestException as e:
            print("Error occurred while retrieving club links:", str(e))

    def all_data(self, url):
        '''
        Retrieve all club data for the Premier League.
        '''
        try:
            lock = threading.Lock()
            all_club_links = self.all_club_links(url)
            if not all_club_links:
                raise ValueError("No club links found")
            names = {
                "Comp": "Competition",
                "Poss": "Possession",
                "Sh": "Shots",
                "SoT": "Shots Target",
                "CrdY": "Yellow",
                "CrdR": "Red",
                "Fls": "Fouls",
                "Off": "Offside",
            }
            result = pd.DataFrame()

            with concurrent.futures.ThreadPoolExecutor() as executor:
                club_tasks = [
                    executor.submit(self.club_data, link)
                    for link in all_club_links
                ]

                for future in concurrent.futures.as_completed(club_tasks):
                    club_data = future.result()
                    if club_data is not None:
                        with lock:
                            result = pd.concat(
                                [result, club_data],
                                axis=0,
                                ignore_index=True,
                            )
            result.rename(columns=names, inplace=True)
            teamName = {
                "Newcastle Utd": "Newcastle United",
                "Nott'ham Forest": "Nottingham Forest",
                "Wolverhampton Wanderers": "Wolves",
                "Brighton and Hove Albion": "Brighton",
                "Manchester Utd": "Manchester United",
                "Tottenham": "Tottenham Hotspur",
                "West Ham": "West Ham United"
            }
            result.replace(teamName, inplace=True)
            return result
        
        except requests.exceptions.RequestException as e:
            print("Error occurred while retrieving club data:", str(e))
        except ValueError as e:
            print("No club links found:", str(e))

    def additional_data(self, response_data, param, match, keepList):
        '''
        Retrieve additional data for a specific club.
        '''
        try:
            soup = BeautifulSoup(response_data.text, "html.parser")
            all_links = soup.find_all("a")
            links = [l.get("href") for l in all_links if l.get("href")]
            links = [l for l in links if param in l]
            if not links:
                raise ValueError("No additional data links found")
            links = "https://fbref.com" + links[0]
            time.sleep(random.randint(10, 30))
            response = self.session.get(links)
            response.raise_for_status() 
            stats = pd.read_html(response.text, match=match)[0]
            stats.columns = stats.columns.droplevel()
            stats = stats[keepList]
            return stats[:-1]
        except requests.exceptions.RequestException as e:
            print("Error occurred while retrieving additional data:", str(e))
        except ValueError as e:
            print("No additional data links found:", str(e))

    def club_data(self, link):
        '''
        Retrieve club data for a specific club.
        '''
        try:
            time.sleep(random.randint(10, 30))
            response = self.session.get(link)

            #check for network errors
            response.raise_for_status()  
            clubName = link.split("/")[-1].replace("-Stats", "").replace("-", " ")
            print(f"Getting Data for {clubName}")
            scores = pd.read_html(response.text, match="Scores & Fixtures")[0]
            scores = scores[
                [
                    "Date",
                    "Comp",
                    "Day",
                    "Venue",
                    "Result",
                    "GF",
                    "GA",
                    "Opponent",
                    "Poss",
                ]
            ]
            shooting = self.additional_data(
                response,
                "/all_comps/shooting/",
                "Shooting",
                ["Date", "Sh", "SoT"],
            )
            time.sleep(random.randint(10, 30))
            misc = self.additional_data(
                response,
                "/all_comps/misc/",
                "Miscellaneous",
                ["Date", "CrdY", "CrdR", "Fls", "Off"],
            )
            time.sleep(random.randint(10, 30))
            finalClubData = scores.merge(shooting, how="left").merge(
                misc, how="left"
            )
            finalClubData = finalClubData[
                finalClubData["Comp"] == "Premier League"
            ]
            finalClubData["Team"] = clubName
            finalClubData["Date"] = pd.to_datetime(
                finalClubData["Date"], format="%Y-%m-%d"
            )
            int_columns = ["Poss", "Sh", "SoT", "CrdY", "CrdR", "Fls", "Off"]
            finalClubData[int_columns] = finalClubData[int_columns].astype(int)
            print(f"Data for {clubName} gathered")
            return finalClubData
        except requests.exceptions.RequestException as e:
            print("Error occurred while retrieving club data: ", str(e))



class Command(BaseCommand):

    '''
    Custom management command to replace instances of the model.
    '''

    def handle(self, *args, **options):
        '''
        Replaces and populates the model instances with the data from the csv file.
        '''
        print(f'Starting data scraping at {timezone.make_aware(datetime.now())}')
        table = AllLeagueData()
        res = table.all_data(table.get_url())
        print("New data has been created.")

        def deleteEntireModel():
            TableModel.objects.all().delete()

        deleteEntireModel()

        for _, row in res.iterrows():
            TableModel.objects.create(Date=row['Date'], Competition=row['Competition'], 
                              Day=row['Day'], Venue=row['Venue'], Result=row['Result'],
                              GF=row['GF'], GA=row['GA'], Opponent=row['Opponent'],
                              Possession=row['Possession'], Shots=row['Shots'], Shots_Target=row['Shots Target'],
                              Yellow=row['Yellow'], Red=row['Red'], Fouls=row['Fouls'],
                              Offside=row['Offside'], Team=row['Team'])
            
        print('Message : All instances of the model have been replaced with new data.')