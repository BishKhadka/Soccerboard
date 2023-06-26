import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import concurrent.futures
import time
import threading


class LeagueTable(object):

    def __init__(self, league):
        '''
        Initialize the LeagueTable object with the given league name.
        '''
        self.league_name = league
        self.url = ""

    def get_url(self):
        '''
        Retrieve the URL for the specified league.
        '''
        leagues = {
            "serie a": "https://fbref.com/en/comps/11/Serie-A-Stats",
            "premier league": "https://fbref.com/en/comps/9/Premier-League-Stats",
            "laliga": "https://fbref.com/en/comps/12/La-Liga-Stats",
            "bundesliga": "https://fbref.com/en/comps/20/Bundesliga-Stats",
            "ligue 1": "https://fbref.com/en/comps/13/Ligue-1-Stats",
        }
        return leagues.get(self.league_name.lower(), "")

    def get_table(self):
        '''
        Retrieve the league table data for the specified league.
        '''
        try:
            url = self.get_url()
            if not url:
                raise ValueError("Invalid league name")
            response = requests.get(url)
            response.raise_for_status()  # Check for network errors
            club = response.text
            scores = pd.read_html(club, match="Regular season Table")[0]
            keep = [
                "Rk",
                "Squad",
                "MP",
                "W",
                "D",
                "L",
                "GF",
                "GD",
                "Pts",
                "Top Team Scorer",
            ]
            scores = scores[keep]
            names = {"Rk": "Rank", "Squad": "Team", "Pts": "Points"}
            scores.rename(columns=names, inplace=True)
            return scores
        except requests.exceptions.RequestException as e:
            print("Error occurred while retrieving league table: ", str(e))
        except ValueError as e:
            print("Invalid league name: ", str(e))


class AllLeagueData(object):
    def __init__(self):
        '''
        Initialize the AllLeagueData object.
        '''
        self.url = "https://fbref.com/en/comps/9/Premier-League-Stats"

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
            response = requests.get(url)
            response.raise_for_status()  # Check for network errors
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

    def additional_data(self, requestData, param, match, keepList):
        '''
        Retrieve additional data for a specific club.
        '''
        try:
            soup = BeautifulSoup(requestData.text, "html.parser")
            all_links = soup.find_all("a")
            links = [l.get("href") for l in all_links if l.get("href")]
            links = [l for l in links if param in l]
            if not links:
                raise ValueError("No additional data links found")
            links = "https://fbref.com" + links[0]
            time.sleep(random.randint(10, 35))
            response = requests.get(links)
            response.raise_for_status()  # Check for network errors
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
            time.sleep(random.randint(10, 35))
            response = requests.get(link)

            #check for network errors
            response.raise_for_status()  
            club = response.text
            clubName = link.split("/")[-1].replace("-Stats", "").replace("-", " ")
            print(f"Getting Data for {clubName}")
            scores = pd.read_html(club, match="Scores & Fixtures")[0]
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
                club,
                "/all_comps/shooting/",
                "Shooting",
                ["Date", "Sh", "SoT"],
            )
            time.sleep(random.randint(10, 35))
            misc = self.additional_data(
                club,
                "/all_comps/misc/",
                "Miscellaneous",
                ["Date", "CrdY", "CrdR", "Fls", "Off"],
            )
            time.sleep(random.randint(10, 35))
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

if __name__ == "__main__":
    table = AllLeagueData()
    res = table.all_data(table.get_url())
    if res is not None:
        res.to_csv("App1/PLData.csv", index=False)
