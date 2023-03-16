# %%
import numpy as np
import os
import json
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt


# %%
# Load Datasets & add session name
def LoadData(count):
    name = FileList[count]
    datastring = '/Data/'
    saveLocation = dir + datastring + name
    with open(saveLocation) as f:
        data = json.load(f)
        data['Session'] = name
    dataSS = pd.json_normalize(data, 'ScoredSteps')
    dataSS['GameSessionId'] = data['Session']
    return dataSS

# Define a function to convert time from string to epoch time
def to_epoch(time_str):
    dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
    return int(dt.timestamp())

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

# Commented code for parquet file generation
# newdata.to_parquet(time.strftime("%Y%m%d-%H%M%S") + '.parquet')

#%%
# Loading new DF for Daan runs with search
daandf = newdata
daandf1 = daandf[daandf['GameSessionId'].str.contains('Run_Daan1')]
daandf2 = daandf[daandf['GameSessionId'].str.contains('Run_Daan2')]

# Apply the function to the time column in your DataFrame
daandf1['SecondsFromStart'] = daandf1['StopTime'].apply(to_epoch)
daandf1['SecondsFromStart'] = daandf1['SecondsFromStart'] - daandf1['SecondsFromStart'].iloc[0]

# Filter by columns that have scoring
daandf1 = daandf1.query("`StartScore` >= 1")

# Plotting
# x=daandf["SecondsFromStart"]
# y1=daandf["StartScore"].cumsum()
# y2=daandf["Penalty"].cumsum()
# plt.style.use('_mpl-gallery')
# fig, ax = plt.subplots()
# ax.stackplot(x, [y1, y2])
# fig.set_size_inches(20, 10)
# plt.gca().invert_yaxis()
# plt.xlabel("Time (s)")
# plt.ylabel("Penalty/Total")
# plt.show()

# Define x, y1, and y2
x = daandf1["SecondsFromStart"]
y1 = daandf1["StartScore"].cumsum()
y2 = daandf1["Penalty"].cumsum()

# Create a stacked area plot with labels and legend
plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()
ax.stackplot(x, y1, y2, labels=['Daans Penalty Run 1', 'Total Penalty Run 1'])
fig.set_size_inches(20, 10)

# Invert y-axis and set axis labels
plt.gca().invert_yaxis()
plt.xlabel("Time (s)")
plt.ylabel("Penalty/Total")

# Add legend
plt.legend(loc='upper left')

# Show the plot
plt.show()

# %%
