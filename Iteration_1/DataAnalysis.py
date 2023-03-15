# %%
import os
import json
import pandas as pd
from datetime import time, datetime


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

    # call function
    dataSS = ActionTime(dataSS)
    # dataSS = pd.concat([timeDelta, dataSS])
    return dataSS

# %%
# Add column for the time between actions


def ActionTime(data):
    timeDelta = []
    startTime = data["StartTime"][0]
    startTime = startTime[11::]
    startTime = datetime.strptime(startTime, '%H:%M:%S')
    stopTime = data["StopTime"]
    for time in stopTime:
        time = time[11::]
        time = datetime.strptime(time, '%H:%M:%S')
        time = time - startTime
        timeDelta.append(str(time))
    data["TimeDelta"] = timeDelta
    return data


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
