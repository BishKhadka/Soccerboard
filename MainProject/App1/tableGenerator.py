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

    def getAllClubLinks(url):
        #get the response
        response = requests.get(url)
        soup = BeautifulSoup(response.text)
        
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
                        print(result)
        result.rename(columns=names, inplace=True)  # Rename columns
        return result

    def getAdditionalData(requestData, param, match, keepList):
        soup = BeautifulSoup(requestData.text)
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
        print(clubName)

        # get Scores (on the same page)
        scores = pd.read_html(club.text, match = "Scores & Fixtures")[0]
        scores = scores[['Date', 'Time', 'Comp', 'Day', 'Venue', 'Result', 'GF', 'GA','Opponent', 'Poss']]

        # get shooting and other stat (figure better ways for these two)
        shooting = self.getAdditionalData(club, "/all_comps/shooting/", "Shooting", ['Date', 'Sh', "SoT"])
        time.sleep(random.randint(10,35))
        misc = self.getAdditionalData(club, "/all_comps/misc/", "Miscellaneous", ['Date', 'CrdY', 'CrdR', 'Fls', 'Off'])
        time.sleep(random.randint(10,35))

    #     names = {"Comp": "Competition", "Poss": "Possession", "Sh":"Shots", "SoT":"Shots Target", "CrdY":"Yellow", "CrdR":"Red", "Fls":"Fouls","Off":"Offside"}
        finalClubData = scores.merge(shooting, how='left').merge(misc, how='left')
    #     finalClubData.rename(columns=names, inplace=True)
        finalClubData = finalClubData[finalClubData["Comp"] == "Premier League"]
        finalClubData["Team"] = clubName
        print(clubName)
        return finalClubData

#download the data
#create table object
table = LeagueTable()
res = table.getClubData(table.getUrl())
res.to_csv("PLData.csv", index = False)