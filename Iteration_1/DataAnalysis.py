# %%
import os
import json
import pandas as pd
import time



# %%
# Load Datasets & add session name
def LoadData(count):
    name = FileList[count]
    saveLocation = dir + "\Data\\" + name
    with open(saveLocation) as f:
        data = json.load(f)
        data['Session'] = name
    dataSS = pd.json_normalize(data, 'ScoredSteps')
    dataSS['GameSessionId'] = data['Session']
    return dataSS


# %%
# Interactive windows have diff dir's
pathExtension = "Iteration_1"
dir = os.getcwd()
pathCheck = dir.endswith(pathExtension)
if not pathCheck:
    os.chdir(pathExtension)
    dir = os.getcwd()

# %%
# Grab datasets and initiate function to load data
pathToJson = "Data/"
FileList = [pos_json for pos_json in os.listdir(
    pathToJson) if pos_json.endswith('.json')]

count = len(FileList)
while count > 0:
    count = count - 1
    newdata = LoadData(count)
    if count != len(FileList) - 1:
        newdata = pd.concat([olddata, newdata])
        newdata = newdata.drop(columns=['Id'])
    olddata = newdata
del olddata

# ActionScore
dataAS = newdata['ActionScores']

newdata.to_parquet(time.strftime("%Y%m%d-%H%M%S") + '.parquet')