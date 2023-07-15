import requests
import pandas as pd
import requests

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
            "la liga": "https://fbref.com/en/comps/12/La-Liga-Stats",
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