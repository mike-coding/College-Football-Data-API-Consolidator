import pandas as pd
import requests

class GameRetriever:
    
    def __init__(self, startYear):
        self.startYear = startYear
        self.baseURL = "https://api.collegefootballdata.com/"
        self.endPoint = "games"
        self.headers = {'Authorization': "Bearer [omitted]"}
    
    def get_games(self):
        looseFrames = []
        for targetYear in range(self.startYear,2024):
            print(f'Progress: ~{round((len(looseFrames)/(2024-self.startYear))*100,2)}%')
            fullQuery= f"{self.baseURL}{self.endPoint}?year={targetYear}"
            yearFrame = self.perform_query(fullQuery)
            looseFrames.append(yearFrame)  
        looseFrames = [frame for frame in looseFrames if frame is not None]
        fullFrame = pd.concat(looseFrames,ignore_index=True)
        filteredFrame = GameRetriever.process_frame(fullFrame)
        return filteredFrame

    @staticmethod
    def get_drop_columns():
        gameColumns = ["start_time_tbd","completed","venue","highlights","notes"]
        teamColumns = ["home_line_scores","home_post_win_prob","home_postgame_elo"]
        teamColumns = [x for column in teamColumns for x in (column.replace('home','away'), column)]
        return gameColumns+teamColumns
        
    def perform_query(self, query):
        response = requests.get(query, headers=self.headers)
        if response.status_code == 200:
            print('connection successful')
            thisYear = response.json()
            return (pd.DataFrame(thisYear))
        else:
            print(f'response status: {response.status_code}')
            print(f'attempted query: {query}')
            return None

    def perform_additional_drops(dataFrame, toDrop):
        filteredFrame = dataFrame.drop(columns=toDrop)
        return filteredFrame
    
    def process_frame(inputFrame):
        inputFrame.drop(columns=GameRetriever.get_drop_columns(), errors='ignore', inplace=True)
        inputFrame['home_wins'] = (inputFrame['home_points'] > inputFrame['away_points']).astype(int)
        return inputFrame
