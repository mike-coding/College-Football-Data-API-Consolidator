import pandas as pd
import requests
from urllib.parse import quote_plus
import time

class TeamStatRetriever:
    baseURL="https://api.collegefootballdata.com/stats/season?team="
    headers = {'Authorization': "Bearer [omitted]"}

    def get_all_team_stats(teams):
        n = len(teams)
        teamData={}
        i=0
        for teamName in teams:
            if teamName not in teamData:
                    team_query = quote_plus(teamName)
                    response = requests.get(f'{TeamStatRetriever.baseURL}{team_query}', headers=TeamStatRetriever.headers)
                    responseData = response.json()
                    teamData[teamName] = responseData
                    time.sleep(0.25)
            print(f'Processing... {round((i/n)*100,2)}%')
            i+=1
        processedStats = TeamStatRetriever.process_team_stats(teamData)
        return processedStats

    def process_team_stats(teamData):
        all_stats_list = []
        for teamName, statsList in teamData.items():
            if isinstance(statsList, list):
                for stat in statsList:
                    stat['team'] = teamName  # Add team name to each stat record
                    all_stats_list.append(stat)

        allStats = pd.DataFrame(all_stats_list)
        return allStats