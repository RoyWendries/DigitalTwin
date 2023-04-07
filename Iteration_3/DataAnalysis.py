# %%
import os
import json
import pandas as pd
import numpy as np
from datetime import datetime
import time


# %%
# Load Datasets & add session name
def LoadData(count):
    name = fileList[count]
    saveLocation = dir + "\Data\\" + name
    with open(saveLocation) as f:
        data = json.load(f)
        data['Session'] = name
    dataSS = pd.json_normalize(data, 'ScoredSteps')
    dataSS['GameSessionId'] = data['Session']

    # call functions
    dataSS = ActionTime(dataSS)
    dataSS = StepInfo(dataSS)

    return dataSS


# %%
# Add binary columns for linear and nonlinear (+ listner as a derivative)
# and add a column for Step Number

def StepInfo(data):
    data['Linear Step'] = np.where(
        data['StepName'].str.contains('LS') == True, True, False)
    data['Non Linear Step'] = np.where(
        data['StepName'].str.contains('NL') == True, True, False)
    data['Step Number'] = np.where(
        data['StepName'].str.contains('_') == True, data['StepName'], False)
    # Cleanup Step Number
    data['Step Number'] = data['Step Number'].str.extract(
        pat='(\d+)', expand=False)
    return data

# %%
# Add column for the time between actions


def ActionTime(data):
    timeDelta = []
    oldtime = timeFormatting(data["StartTime"][0])
    stopTime = data["StopTime"]
    for time in stopTime:
        time = timeFormatting(time)
        timeDelta.append(str(time-oldtime))
        oldtime = time
    data["TimeDelta"] = timeDelta
    return data


# %%
# Timeformatter for the timedelta column
def timeFormatting(dateTime):
    dateTime = dateTime[11::]
    dateTime = datetime.strptime(dateTime, '%H:%M:%S')
    return dateTime


# %%
# minimal scoreTracking
def minScoreTracking(data):
    sumTotalScore = []
    sumTotalPenalty = []
    groupedData = data.groupby(['GameSessionId'])
    for file in fileList:
        totalScore = 0
        totalPenalty = 0
        df = groupedData.get_group(file)
        for element in df["StartScore"]:
            totalScore += element
        sumTotalScore.append(totalScore)
        for element in df['Penalty']:
            totalPenalty += element
        sumTotalPenalty.append(totalPenalty)

    return sumTotalScore, sumTotalPenalty


# %%
# Dir setup for interactive window usage
pathExtension = "Iteration_3"
dir = os.getcwd()
pathCheck = dir.endswith(pathExtension)
if not pathCheck:
    os.chdir(pathExtension)
    dir = os.getcwd()

# %%
# Grab all datasets in 'Data" folder and initiate function to load data
pathToJson = "Data/"
fileList = [pos_json for pos_json in os.listdir(
    pathToJson) if pos_json.endswith('.json')]

count = len(fileList)
while count > 0:
    count = count - 1
    data = LoadData(count)
    if count != len(fileList) - 1:
        data = pd.concat([olddata, data])
        data = data.drop(columns=['Id','ActionScores'])
    olddata = data
del olddata

minScoreTracking(data)

# # DF to Parquet with current time (commented)
# data.to_parquet(time.strftime("%Y%m%d-%H%M%S") + '.parquet')