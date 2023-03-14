# %%
import json
import pandas as pd
import numpy as np

# %%
# Load Datasets & add session name


def LoadData(count):
    name = FileList[count]
    # uncomment and remove when not using interactive window
    # saveLocation = "./Iteration_1/Data/" + name + ".json"
    saveLocation = "g:/Projects/DigitalTwin/Iteration_1/Data/" + name + ".json"
    with open(saveLocation) as f:
        data = json.load(f)
        data['Session'] = name
    dataSS = pd.json_normalize(data, 'ScoredSteps')
    dataSS['GameSessionId'] = data['Session']
    return dataSS


# %%
# Choose datasets and initiate functions
FileList = ['test', 'Run_Daan', 'RoysUnfinishedRun']

count = len(FileList)
while count > 0:
    count = count - 1
    newdata = LoadData(count)
    if count != len(FileList) - 1:
        newdata = pd.concat([olddata, newdata])
        newdata = newdata.drop(columns=['Id'])
    olddata = newdata


# %%
'''
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
# Merged_SS.to_parquet('C:/Users/randy/Downloads/Merged_SS.parquet')
print(Merged_SS['GameSessionId'].nunique())
print(Merged_SS['StepId'].value_counts())
'''

# %%