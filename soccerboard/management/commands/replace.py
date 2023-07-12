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
        self.leagues = {
            "serie a": "https://fbref.com/en/comps/11/Serie-A-Stats",
            "premier league": "https://fbref.com/en/comps/9/Premier-League-Stats",
            "la liga": "https://fbref.com/en/comps/12/La-Liga-Stats",
            "bundesliga": "https://fbref.com/en/comps/20/Bundesliga-Stats",
            "ligue 1": "https://fbref.com/en/comps/13/Ligue-1-Stats",
        }
        self.curr_league = ""
        self.session = requests.Session()
    
    def get_leagures(self):
        '''
        Returns link to all top 5 leagues
        '''
        return self.leagues

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

    def club_data(self, link):
        '''
        Retrieve club data for a specific club.
        '''

        try:
            
            time.sleep(random.randint(20, 60))
            response = self.session.get(link)

            #check for network errors
            response.raise_for_status()
            clubName = link.split(
                "/")[-1].replace("-Stats", "").replace("-", " ")
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
                    "Poss"
                ]
            ]

            shooting = self.additional_data(
                response,
                "/all_comps/shooting/",
                "Shooting",
                ["Date", "Sh", "SoT"],
            )
            time.sleep(random.randint(20, 60))
            misc = self.additional_data(
                response,
                "/all_comps/misc/",
                "Miscellaneous",
                ["Date", "CrdY", "CrdR", "Fls", "Off"],
            )

            #merge both data 
            finalClubData = scores.merge(shooting, how="left").merge(
                misc, how="left"
            )
            
            #renaming columns
            finalClubData["Team"] = clubName

            #check which league it is for
            if self.curr_league == "serie a":
                finalClubData = finalClubData[finalClubData["Comp"] == "Serie A"]
                finalClubData.replace({"Milan": "AC Milan",
                                    "Internazionale": "Inter Milan"},
                                    inplace=True)

            elif self.curr_league == "bundesliga":
                finalClubData = finalClubData[finalClubData["Comp"]
                                            == "Bundesliga"]
                finalClubData.replace({"Köln": "Koln",
                                    "Leverkusen": "Bayer Leverkusen",
                                    "M'Gladbach": "Monchengladbach",
                                    "Eint Frankfurt": "Eintracht Frankfurt"},
                                    inplace=True)

            elif self.curr_league == "premier league":
                finalClubData = finalClubData[finalClubData["Comp"]
                                            == "Premier League"]
                finalClubData.replace({"Newcastle Utd": "Newcastle United",
                                    "Nott'ham Forest": "Nottingham Forest",
                                    "Wolverhampton Wanderers": "Wolves",
                                    "Brighton and Hove Albion": "Brighton",
                                    "Manchester Utd": "Manchester United",
                                    "Tottenham": "Tottenham Hotspur",
                                    "West Ham": "West Ham United"},
                                    inplace=True)
                
            elif self.curr_league == "ligue 1":
                finalClubData = finalClubData[finalClubData["Comp"] == "Ligue 1"]
                finalClubData.replace({"Paris S-G": "Paris Saint Germain"},
                                    inplace=True)

            elif self.curr_league == "la liga":
                finalClubData = finalClubData[finalClubData["Comp"] == "La Liga"]
                finalClubData.replace({"Atlético Madrid": "Atletico Madrid",
                                    "Betis": "Real Betis",
                                    "Cádiz": "Cadiz"},
                                    inplace=True)
            
            finalClubData["Date"] = pd.to_datetime(
                finalClubData["Date"], format="%Y-%m-%d"
            )
            int_columns = ["Poss", "Sh", "SoT", "CrdY", "CrdR", "Fls", "Off"]
            finalClubData[int_columns] = finalClubData[int_columns].astype(int)
            
                
            print(f"Data for {clubName} gathered")
            return finalClubData

        except requests.exceptions.RequestException as e:
            print("Error occurred while retrieving club data: ", str(e))

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
            time.sleep(random.randint(20, 60))
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

    def all_data(self, url):
        '''
        Retrieve all club data for the specified league.
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

            #parallel programming: gather data for clubs in parallel
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
            return result
        
        except requests.exceptions.RequestException as e:
            print("Error occurred while retrieving club data:", str(e))
        except ValueError as e:
            print("No club links found:", str(e))
    
        

class Command(BaseCommand):

    '''
    Custom management command to replace instances of the model.
    '''

    def handle(self, *args, **options):
        '''
        Replaces and populates the model instances with the data from the csv file.
        '''
        print(
            f'Starting data scraping at {timezone.make_aware(datetime.now())}')
        
        table = AllLeagueData()
        final_result = pd.DataFrame()
        
        #get data for each league
        for league in table.leagues:
            url = table.leagues[league]
            table.curr_league = league
            league_data = table.all_data(url)
            final_result = pd.concat(
                                [league_data, final_result],
                                ignore_index=True,
                            )
        print("New data for top 5 leagues created.")

        #update the old data with the new one
        if final_result is not None:
            def delete_entire_model():
                TableModel.objects.all().delete()

            delete_entire_model()

            for _, row in final_result.iterrows():
                TableModel.objects.create(
                    Date=row['Date'],
                    Competition=row['Competition'],
                    Day=row['Day'],
                    Venue=row['Venue'],
                    Result=row['Result'],
                    GF=row['GF'],
                    GA=row['GA'],
                    Opponent=row['Opponent'],
                    Possession=row['Possession'],
                    Shots=row['Shots'],
                    Shots_Target=row['Shots Target'],
                    Yellow=row['Yellow'],
                    Red=row['Red'],
                    Fouls=row['Fouls'],
                    Offside=row['Offside'],
                    Team=row['Team'])

            print('Message : All instances of the model have been replaced with new data.')