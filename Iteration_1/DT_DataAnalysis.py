import json
import pandas as pd
import numpy as np

with open('data/test.json') as f:
    DataRandy = json.load(f)
    DataRandy['Session'] = 'Test'

with open('data/Run_Daan.json') as j:
    DataDaan = json.load(j)
    DataDaan['Session'] = 'Run_Daan'
with open('/data/RoysUnfinishedRun.json') as z:
    DataRoy = json.load(z)
    DataRoy['Session'] = 'RoysUnfinishedRun'


# scored steps df
SSRandy = pd.json_normalize(DataRandy, 'ScoredSteps')
SSRandy['GameSessionId'] = DataRandy['Session']
SSDaan = pd.json_normalize(DataDaan, 'ScoredSteps')
SSDaan['GameSessionId'] = DataDaan['Session']
SSRoy = pd.json_normalize(DataRoy, 'ScoredSteps')
SSRoy['GameSessionId'] = DataRoy['Session']
Merged_SS = pd.concat([SSRandy, SSDaan, SSRoy], keys=[
                      DataRandy['UserId'], DataDaan['UserId'], DataRoy['UserId']])
Merged_SS = Merged_SS.drop(columns=['Id'])

# ActionScores
ASRandy = pd.json_normalize(DataRandy['ScoredSteps'], 'ActionScores')
ASDaan = pd.json_normalize(DataDaan['ScoredSteps'], 'ActionScores')
ASRoy = pd.json_normalize(DataRoy['ScoredSteps'], 'ActionScores')

# Experience
ExpRandy = pd.json_normalize(DataRandy, 'Experience')
ExpDaan = pd.json_normalize(DataDaan, 'Experience')
ExpRoy = pd.json_normalize(DataRoy, 'Experience')

# Testing
Merged_SS.to_parquet('C:/Users/randy/Downloads/Merged_SS.parquet')
print(Merged_SS['GameSessionId'].nunique())
print(Merged_SS['StepId'].value_counts())
