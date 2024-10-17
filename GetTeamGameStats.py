import pandas as pd
import requests
import time

class TeamGameStatRetriever:
    baseURL="https://api.collegefootballdata.com/games/teams?year="
    headers = {'Authorization': "Bearer [omitted]"}

    def get_all_team_game_stats(startYear, endYear):
        weeks = range(1,16)
        years = range(startYear,endYear)
        gameStatsByYear = {}
        totalWeeks= 15 * (endYear-(startYear-1))
        completedWeeks=0
        for year in years:
            gameStatsByWeek = {}
            for week in weeks:
                response = requests.get(f'{TeamGameStatRetriever.baseURL}{year}&week={week}', headers=TeamGameStatRetriever.headers)
                responseData = response.json()
                gameStatsByWeek[week] = responseData
                completedWeeks +=1
                print(f'Processing... {round((completedWeeks/totalWeeks)*100,2)}%')
                time.sleep(0.25)
            gameStatsByYear[year] = gameStatsByWeek
        processedStats = TeamGameStatRetriever.process_team_game_stats(gameStatsByYear)
        return processedStats

    def process_team_game_stats(gameStatsByYear):
        dfList = []
        for year, weekStats in gameStatsByYear.items():
            for week, games in weekStats.items():
                for game in games:
                    for team in game['teams']:
                        teamWeekDict={
                            'season': year,
                            'team': team['school'],
                            'week': week
                        }
                        for stat in team['stats']:
                            teamWeekDict[stat['category']] = stat['stat']
                        dfList.append(teamWeekDict)
        processedTeamGameStats = pd.DataFrame(dfList)
        return processedTeamGameStats
    
