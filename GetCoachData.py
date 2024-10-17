import requests
import pandas as pd
import ast

class CoachRetriever:
    
    baseURL="https://api.collegefootballdata.com/"
    headers = {'Authorization': "Bearer [omitted]"}

    def get_coach_data(startYear, endYear):
        # API call
        targetURL= f'{CoachRetriever.baseURL}coaches?startYear={startYear}&endYear={endYear-1}'
        response = requests.get(targetURL,headers=CoachRetriever.headers)
        responseData = response.json()
        coachData = pd.DataFrame(responseData)

        # Apply the function to the 'seasons' column
        coachData['seasons'] = coachData['seasons']
        coachData = coachData.explode('seasons')
        coachData.reset_index(drop=True,inplace=True)
        seasons_data = pd.json_normalize(coachData['seasons'])
        coachData.drop(columns=['seasons','hire_date'],inplace=True)
        coachData = pd.concat([coachData, seasons_data],axis=1)
        coachData.drop(columns=['preseason_rank', 'postseason_rank', 'srs', 'sp_overall','sp_offense','sp_defense'],inplace=True)
        return coachData