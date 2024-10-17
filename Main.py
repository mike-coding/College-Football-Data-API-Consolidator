from GetGames import GameRetriever
from GetCoachData import CoachRetriever
from GetTeamStats import TeamStatRetriever
from GetTeamGameStats import TeamGameStatRetriever
from GameExpansion import GameMapper
import requests
import pandas as pd
import os

## GENERAL API SETTINGS
key="[omitted]"
prefix="Bearer "
baseURL="https://api.collegefootballdata.com/"
headers = {'Authorization': prefix + key}

## path settings
path = 'C:\\Users\\Admin\\SamplePath'

## other general settings
startYear = 2004
endYear = 2024

## Funcs
def Main():
    #run functions as needed here
    pass

def dropIndex(fileName):
    df = pd.read_csv(path+fileName)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])
    df.to_csv(path+fileName,index=False)

def loadData(step):
    if step==1:
        return pd.read_csv(path+'1.raw_Games.csv')
    if step==2:
        return pd.read_csv(path+'2.raw_Coaches.csv')
    if step==3:
        return pd.read_csv(path+'3.raw_Team_Stats.csv')
    if step==4:
        return pd.read_csv(path+'4.raw_Team_Game_Stats.csv')
    if step==5:
        return pd.read_csv(path+'5.mapped_Coach_Records_Games.csv')
    if step==6:
        return pd.read_csv(path+'6.mapped_Team_Records_Games.csv')
    if step==7:
        return pd.read_csv(path+'7.mapped_Team_Season_Stats.csv')
    if step==8:
        return pd.read_csv(path+'8.mapped_Team_Game_Stats.csv')

def getGameData(write):
    gameRetriever = GameRetriever(startYear)
    allGames = gameRetriever.get_games()
    if write:
        allGames.to_csv(path+'1.raw_Games.csv',index=False)
    return allGames

def getCoachData(write):
    allCoach = CoachRetriever.get_coach_data(startYear,endYear)
    if write:
        allCoach.to_csv(path+'2.raw_Coaches.csv',index=False)
    return allCoach

def getTeamStatData(rawGames, write):
    unique_teams = pd.unique(rawGames[['home_team', 'away_team']].values.ravel())
    allTeamStats = TeamStatRetriever.get_all_team_stats(unique_teams)
    if write:
        allTeamStats.to_csv(path+'3.raw_Team_Stats.csv',index=False)
    return allTeamStats

def getTeamGameStatData(write):
    allTeamGameStats = TeamGameStatRetriever.get_all_team_game_stats(startYear,endYear)
    if write:
        allTeamGameStats.to_csv(path+'4.raw_Team_Game_Stats.csv',index=False)
    return allTeamGameStats

def mapGamesToCoachRecords(write):
    games = loadData(1)
    coaches = loadData(2)
    coachGameMap = GameMapper.get_coach_career_to_date_stats(games,coaches)
    if write:
        coachGameMap.to_csv(path+'5.mapped_Coach_Records_Games.csv',index=False)
    return coachGameMap

def mapGamesToTeamRecords(write):
    games = loadData(1)
    teamRecordGameMap = GameMapper.get_team_history_to_date_stats(games)
    if write:
        teamRecordGameMap.to_csv(path+'6.mapped_Team_Records_Games.csv', index=False)
    return teamRecordGameMap

def mapGamesToTeamSeasonStats(write):
    games= loadData(1)
    teamSeasonStats = loadData(3)
    teamSeasonStats = GameMapper.get_team_season_stats(games, teamSeasonStats)
    if write:
        teamSeasonStats.to_csv(path+'7.mapped_Team_Season_Stats.csv', index= False)
    return teamSeasonStats

def mapGamesToTeamGameStats(write):
    games= loadData(1)
    teamGameStats = loadData(4)
    teamGameStats = GameMapper.get_team_game_stats(games, teamGameStats)
    if write:
        teamGameStats.to_csv(path+'8.mapped_Team_Game_Stats.csv', index= False)
    return teamGameStats

def probethirdDownEff():
    teamGameStats = loadData(4)
    thirdDownEff = teamGameStats['thirdDownEff']
    for value in thirdDownEff:
        print(value)

def performFullMap(write):
    stepToFrameDict = {}
    for i in [1,5,6,7,8]:
        stepToFrameDict[i]=loadData(i)
    finalDF = GameMapper.join_frames(stepToFrameDict)
    if write:
        finalDF.to_csv(path+'9.final.csv', index=False)
    return finalDF

def handleMissingValues(overWrite, file):
    df = pd.read_csv(path+file)
    df.fillna('?', inplace = True)
    if overWrite:
        df.to_csv(path+file,index=False)
    return df

Main()