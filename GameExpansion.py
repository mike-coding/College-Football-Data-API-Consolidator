import pandas as pd
import numpy as np
class GameMapper:

    def get_coach_career_to_date_stats(rawGames, rawCoaches):
        newMap = []
        for row in rawGames.itertuples():
            year = row.season
            teams = {"home":row.home_team,"away":row.away_team}
            gameID = row.id
            newRow={'id':gameID}
            for homeAway, teamName in teams.items():
                coachRow = rawCoaches[(rawCoaches['year']==year) & (rawCoaches['school']==teamName)]
                if not coachRow.empty:
                    coachFirst = coachRow.iloc[0]['first_name']
                    coachLast = coachRow.iloc[0]['last_name']
                    newRow[f'{homeAway}_coach'] = f'{coachFirst} {coachLast}'
                else:
                    # Handle case where coach data is not found
                    print(f"Warning: No coach data found for {teamName} in {year}. Skipping.")
                    newRow[f'{homeAway}_coach'] = None
                    newRow[f'{homeAway}_coach_career_games'] = None
                    newRow[f'{homeAway}_coach_career_win_rate'] = None
                    newRow[f'{homeAway}_coach_five_year_games'] = None
                    newRow[f'{homeAway}_coach_five_year_win_rate'] = None
                    newRow[f'{homeAway}_coach_ten_year_games'] = None
                    newRow[f'{homeAway}_coach_ten_year_win_rate'] = None
                    continue
                coachFirst = coachRow.iloc[0]['first_name']
                coachLast = coachRow.iloc[0]['last_name']
                newRow[f'{homeAway}_coach']=f'{coachFirst} {coachLast}'

                coachCareerToDateFrame = rawCoaches[(rawCoaches['first_name']==coachFirst) & (rawCoaches['last_name']==coachLast) & (rawCoaches['year']<year)]
                (careerGames, careerWinRate) = GameMapper.get_total_games_win_rate(coachCareerToDateFrame)
                newRow[f'{homeAway}_coach_career_games'] = careerGames
                newRow[f'{homeAway}_coach_career_win_rate'] = careerWinRate

                coachFiveYearToDateFrame = coachCareerToDateFrame[(coachCareerToDateFrame['year']>year-6)]
                (fiveYearGames, fiveYearWinRate) = GameMapper.get_total_games_win_rate(coachFiveYearToDateFrame)
                newRow[f'{homeAway}_coach_five_year_games'] = fiveYearGames
                newRow[f'{homeAway}_coach_five_year_win_rate'] = fiveYearWinRate

                coachTenYearToDateFrame = coachCareerToDateFrame[(coachCareerToDateFrame['year']>year-11)]
                (tenYearGames, tenYearWinRate) = GameMapper.get_total_games_win_rate(coachTenYearToDateFrame)
                newRow[f'{homeAway}_coach_ten_year_games'] = tenYearGames
                newRow[f'{homeAway}_coach_ten_year_win_rate'] = tenYearWinRate

            newMap.append(newRow)
        coachMap = pd.DataFrame(newMap)
        return coachMap

    def get_total_games_win_rate(coachGames):
        gamesTot=0
        winsTot=0
        for row in coachGames.itertuples():
            gamesTot+= row.games
            winsTot+= row.wins
        if gamesTot!=0:
            return (gamesTot, round((winsTot/gamesTot),2))
        else:
            return (None, None)
        
    def get_team_history_to_date_stats(rawGames):
        newMap = []
        rowCount=0
        maxRow=33345
        for row in rawGames.itertuples():
            year = row.season
            teams = {"home":row.home_team,"away":row.away_team}
            gameID = row.id
            newRow={'id':gameID}
            for homeAway, teamName in teams.items():
                homeTeamGames = rawGames[(rawGames['home_team']==teamName) & (rawGames['season']<year)]
                awayTeamGames = rawGames[(rawGames['away_team']==teamName)& (rawGames['season']<year)]

                totalTeamWinRateToDate = GameMapper.get_team_win_rate(awayTeamGames,homeTeamGames)
                newRow[f'{homeAway}_total_WR_to_date']=totalTeamWinRateToDate

                lastSZNhomeTeamGames = homeTeamGames[(homeTeamGames['season']==year-1)]
                lastSZNawayTeamGames = awayTeamGames[(awayTeamGames['season']==year-1)]
                lastSZNTeamWinRate = GameMapper.get_team_win_rate(lastSZNawayTeamGames,lastSZNhomeTeamGames)
                newRow[f'{homeAway}_SZN-1_WR'] = lastSZNTeamWinRate

                SZNSub2homeTeamGames = homeTeamGames[(homeTeamGames['season']==year-2)]
                SZNSub2awayTeamGames = awayTeamGames[(awayTeamGames['season']==year-2)]
                SZNSub2TeamWinRate = GameMapper.get_team_win_rate(SZNSub2awayTeamGames,SZNSub2homeTeamGames)
                if (SZNSub2TeamWinRate != None) & (lastSZNTeamWinRate != None):
                    newRow[f'{homeAway}_SZN-2_WR'] = round(((SZNSub2TeamWinRate+lastSZNTeamWinRate)/2),2)
                else:
                    newRow[f'{homeAway}_SZN-2_WR'] = None

                SZNSub3homeTeamGames = homeTeamGames[(homeTeamGames['season']==year-3)]
                SZNSub3awayTeamGames = awayTeamGames[(awayTeamGames['season']==year-3)]
                SZNSub3TeamWinRate = GameMapper.get_team_win_rate(SZNSub3awayTeamGames,SZNSub3homeTeamGames)
                if (SZNSub3TeamWinRate != None) & (SZNSub2TeamWinRate != None) & (lastSZNTeamWinRate != None):
                    newRow[f'{homeAway}_SZN-3_WR'] = round(((SZNSub3TeamWinRate+SZNSub2TeamWinRate+lastSZNTeamWinRate)/3),2)
                else:
                    newRow[f'{homeAway}_SZN-3_WR'] = None

                SZNSub4homeTeamGames = homeTeamGames[(homeTeamGames['season']==year-4)]
                SZNSub4awayTeamGames = awayTeamGames[(awayTeamGames['season']==year-4)]
                SZNSub4TeamWinRate = GameMapper.get_team_win_rate(SZNSub4awayTeamGames,SZNSub4homeTeamGames)
                if (SZNSub4TeamWinRate != None) & (SZNSub3TeamWinRate != None) & (SZNSub2TeamWinRate != None) & (lastSZNTeamWinRate != None):
                    newRow[f'{homeAway}_SZN-4_WR'] = round(((SZNSub4TeamWinRate+SZNSub3TeamWinRate+SZNSub2TeamWinRate+lastSZNTeamWinRate)/4),2)
                else:
                    newRow[f'{homeAway}_SZN-4_WR'] = None

                SZNSub5homeTeamGames = homeTeamGames[(homeTeamGames['season']==year-5)]
                SZNSub5awayTeamGames = awayTeamGames[(awayTeamGames['season']==year-5)]
                SZNSub5TeamWinRate = GameMapper.get_team_win_rate(SZNSub5awayTeamGames,SZNSub5homeTeamGames)
                if (SZNSub5TeamWinRate != None) & (SZNSub4TeamWinRate != None) & (SZNSub3TeamWinRate != None) & (SZNSub2TeamWinRate != None) & (lastSZNTeamWinRate != None):
                    newRow[f'{homeAway}_SZN-5_WR'] = round(((SZNSub5TeamWinRate+SZNSub4TeamWinRate+SZNSub3TeamWinRate+SZNSub2TeamWinRate+lastSZNTeamWinRate)/5),2)
                else:
                    newRow[f'{homeAway}_SZN-5_WR'] = None
            newMap.append(newRow)
            rowCount+=1
            print(f'progress: {round(((rowCount/maxRow)*100),2)}%')
        teamHistoryMap = pd.DataFrame(newMap)
        return teamHistoryMap

    def get_team_win_rate(awayGames, homeGames):
        totGames= len(awayGames)+len(homeGames)
        homeWins = len(homeGames[homeGames['home_wins']==1])
        awayWins = len(awayGames[awayGames['home_wins']==0])
        wins = homeWins+awayWins
        return round((wins/totGames),2) if totGames>0 else None
    
    def get_team_season_stats(rawGames, rawTeamStats):
        newMap = []
        rowCount=0
        maxRow=33345
        for row in rawGames.itertuples():
            year = row.season
            week = row.week
            teams = {"home":row.home_team,"away":row.away_team}
            gameID = row.id
            newRow={'id':gameID}
            for homeAway, teamName in teams.items():
                for i in range(2,7): #checks for years 
                    gameStatWindow = rawTeamStats[(rawTeamStats['season']>year-i) & 
                                               (rawTeamStats['season']<year) & 
                                               (rawTeamStats['team']==teamName)] 
                    statOptions = gameStatWindow['statName'].unique().tolist()
                    statDict = {}
                    for stat in statOptions:
                        statDict[stat]=gameStatWindow[(gameStatWindow['statName']==stat)]['statValue'].mean()
                        newRow[f'{homeAway}_{stat}_{i-1}yr_avg'] = statDict[stat]
            newMap.append(newRow)
            rowCount+=1
            print(f'progress: {round(((rowCount/maxRow)*100),2)}%')
        return pd.DataFrame(newMap)
    
    def get_team_game_stats(rawGames, rawTeamGameStats):
        newMap = []
        rowCount=0
        maxRow=33345
        for row in rawGames.itertuples():
            year = row.season
            week = row.week
            teams = {"home":row.home_team,"away":row.away_team}
            gameID = row.id
            newRow={'id':gameID}
            for homeAway, teamName in teams.items():
                for i in range(week-1,0,-1): #check each week to date
                    gameStatWindow = rawTeamGameStats[(rawTeamGameStats['season']==year) & 
                                               (rawTeamGameStats['team']==teamName) & 
                                               (rawTeamGameStats['week']<=i)]
                    filteredWindow = gameStatWindow.drop(columns=['season', 'team', 'week'])
                    for column in filteredWindow.columns:
                        try:
                            average_value = filteredWindow[column].mean()
                        except:
                            if 'totalPenaltiesYards' in column:
                                values = [x.split('-')[1] if GameMapper.is_valid_split(x,'-') else None for x in filteredWindow[column]]
                                average_value = np.mean([float(x) for x in values if x is not None]) if values else None
                            elif 'possessionTime' in column:
                                values = [x.split(':') if GameMapper.is_valid_split(x,':') else [None, None] for x in filteredWindow[column]]
                                values = [float(x[0])*60 + float(x[1]) if (x[0] != None and x[1] != None) else None for x in values]
                                average_value = np.mean([x for x in values if x is not None]) if values else None
                            else:
                                values = [x.split('-') if GameMapper.is_valid_split(x,'-') else [None,None] for x in filteredWindow[column] ]
                                values = [float(y[0]) / float(y[1]) if (not pd.isna(y[0]) and not pd.isna(y[1]) and float(y[1]) != 0) else None for y in values ]
                                average_value = np.mean([x for x in values if x is not None]) if values else None

                        newRow[f'{homeAway}_{column}_{i}week_avg'] = round(average_value, 2) if not pd.isna(average_value) else None

            newMap.append(newRow)
            rowCount+=1
            print(f'progress: {round(((rowCount/maxRow)*100),2)}%')
        return pd.DataFrame(newMap)
            
    def is_valid_split(input, targetChar):
        if isinstance(input, str) and not pd.isna(input) and input.count(targetChar) == 1:
            return True
        else:
            return False
        
    def join_frames(allFrames):
        games = allFrames[1]
        for i in range(5,9):
            games = games.merge(allFrames[i], on='id', how='left')
        return games
        