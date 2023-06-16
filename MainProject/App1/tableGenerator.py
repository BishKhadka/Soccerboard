# Create your views here.
# from .models import myModel
import csv

import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import concurrent.futures
import time
import threading

class getLeagueTable(object):
    
    def __init__(self, leagueName):
        self.leagueName = leagueName
        self.url = ""
        
    def getUrl(self):
        if self.leagueName.lower() == "serie a":
            self.url = "https://fbref.com/en/comps/11/Serie-A-Stats"
        elif self.leagueName.lower() == "premier league":
            self.url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        elif self.leagueName.lower() == "laliga":
            self.url = "https://fbref.com/en/comps/12/La-Liga-Stats"
        elif self.leagueName.lower() == "bundesliga":
            self.url = "https://fbref.com/en/comps/20/Bundesliga-Stats"
        elif self.leagueName.lower() == "ligue 1":
            self.url = "https://fbref.com/en/comps/13/Ligue-1-Stats"
        return self.url
    
    def getTable(self):
        a = self.getUrl()
        club = requests.get(self.getUrl())
        # get Scores (on the same page)
        scores = pd.read_html(club.text)
        scores = pd.read_html(club.text, match = "Regular season Table")[0]
        keep = ["Rk", "Squad", "MP", "W", "D", "L", "GF", "GD", "Pts", "Top Team Scorer"]        
        scores = scores[keep]
        names = {"Rk": "Rank", "Squad": "Team", "Pts":"Points"}
        scores.rename(columns=names, inplace=True)  # Rename columns
        return scores


# Create your views here.
# from .models import myModel
import csv

import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import concurrent.futures
import time
import threading

class LeagueTable(object):

    def __init__(self):
        self.url = "https://fbref.com/en/comps/9/Premier-League-Stats"
        # table = pd.DataFrame()

    def getUrl(self):
        return self.url
    
    # def getTable(self):
    #     return self.table
    
    # def setTable(self, df):
    #     self.table = df

    def getAllClubLinks(self, url):
        #get the response
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        #select the first table and find all anchor tags
        teamTable = soup.select("table.stats_table")[0]
        teamLinks = teamTable.find_all("a")
        
        #get if link has href and and "/squads/"
        teamLinks = [l.get("href") for l in teamLinks]
        teamLinks = [l for l in teamLinks if "/squads/" in l]
        teamLinks = [f"https://fbref.com{l}" for l in teamLinks]
        print(teamLinks)
        return teamLinks

    def getPLData(self, url):
        lock = threading.Lock()
        # runs only once for all clubs, returns team links
        allClubLinks = self.getAllClubLinks(url)
        names = {"Comp": "Competition", "Poss": "Possession", "Sh":"Shots", "SoT":"Shots Target", "CrdY":"Yellow", "CrdR":"Red", "Fls":"Fouls","Off":"Offside"}
        
        result = pd.DataFrame()  # Initialize an empty dataframe
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            #submit each club processing as a separate task
            club_tasks = [executor.submit(self.getClubData, link) for link in allClubLinks]
            
            # Process the completed tasks as they finish
            for future in concurrent.futures.as_completed(club_tasks):
                club_data = future.result()
                if club_data is not None:
                    with lock:
                        result = pd.concat([result, club_data], axis=0, ignore_index=True)  # Concatenate current club_data with the result dataframe
#                         print(result)

        result.rename(columns=names, inplace=True)  # Rename columns
        teamName = {"Newcastle Utd" : "Newcastle United", "Nott'ham Forest": "Nottingham Forest", "Wolverhampton Wanderers": "Wolves", "Brighton and Hove Albion":"Brighton", "Manchester Utd":"Manchester United", "Tottenham":"Tottenham Hotspur"}
        result.replace(teamName, inplace=True)
        return result

    def getAdditionalData(self, requestData, param, match, keepList):
        soup = BeautifulSoup(requestData.text, 'html.parser')
        all_links = soup.find_all("a")
        links = [l.get("href") for l in all_links]
        links = [l for l in links if l and param in l]
        links = "https://fbref.com" + links[0]
        time.sleep(random.randint(10,35))
        shooting = requests.get(links)
        shooting = pd.read_html(shooting.text, match=match)[0]
        shooting.columns = shooting.columns.droplevel()
        shooting = shooting[keepList]

        return shooting[:-1]

    def getClubData(self,link):
        time.sleep(random.randint(10,35))
        club = requests.get(link)
        clubName = link.split("/")[-1].replace("-Stats","").replace("-", " ")
        print(f'Getting Data for {clubName}')

        # get Scores (on the same page)
        scores = pd.read_html(club.text)
        scores = pd.read_html(club.text, match = "Scores & Fixtures")[0]
        scores = scores[['Date', 'Comp', 'Day', 'Venue', 'Result', 'GF', 'GA','Opponent', 'Poss']]

        # get shooting and other stat (figure better ways for these two)
        shooting = self.getAdditionalData(club, "/all_comps/shooting/", "Shooting", ['Date', 'Sh', "SoT"])
        time.sleep(random.randint(10,35))
        misc = self.getAdditionalData(club, "/all_comps/misc/", "Miscellaneous", ['Date', 'CrdY', 'CrdR', 'Fls', 'Off'])
        time.sleep(random.randint(10,35))

        finalClubData = scores.merge(shooting, how='left').merge(misc, how='left')
        finalClubData = finalClubData[finalClubData["Comp"] == "Premier League"]
        finalClubData["Team"] = clubName
        finalClubData['Date'] = pd.to_datetime(finalClubData['Date'], format='%Y-%m-%d')
        # Convert float columns to int
        int_columns = ["Poss", "Sh","SoT","CrdY","CrdR","Fls","Off"]
        finalClubData[int_columns] = finalClubData[int_columns].astype(int)
        print(f'Data for {clubName} gathered')
        return finalClubData

if __name__ == "__main__":
    table = LeagueTable()
    res = table.getPLData(table.getUrl())
    res.to_csv("App1/PLData.csv", index = False)