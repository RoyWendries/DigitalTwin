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
pathExtension = "Ebbinghaus_code"
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
daandf3 = daandf[daandf['GameSessionId'].str.contains('Run_Daan3')]

# Apply the function to the time column in your DataFrame
daandf1['SecondsFromStart'] = daandf1['StopTime'].apply(to_epoch)
daandf1['SecondsFromStart'] = daandf1['SecondsFromStart'] - daandf1['SecondsFromStart'].iloc[0]
daandf2['SecondsFromStart'] = daandf2['StopTime'].apply(to_epoch)
daandf2['SecondsFromStart'] = daandf2['SecondsFromStart'] - daandf2['SecondsFromStart'].iloc[0] 
daandf3['SecondsFromStart'] = daandf3['StopTime'].apply(to_epoch)
daandf3['SecondsFromStart'] = daandf3['SecondsFromStart'] - daandf3['SecondsFromStart'].iloc[0] 


# Filter by columns that have scoring
daandf1 = daandf1.query("`StartScore` >= 1")
daandf2 = daandf2.query("`StartScore` >= 1")
daandf3 = daandf3.query("`StartScore` >= 1")

# New column for graphing with penalty delta
daandf1['AntiPenalty1'] = daandf1['StartScore'] - daandf1['Penalty']
daandf2['AntiPenalty2'] = daandf2['StartScore'] - daandf2['Penalty']
daandf3['AntiPenalty3'] = daandf3['StartScore'] - daandf3['Penalty']


# Merging dfs
frames = [daandf1, daandf2, daandf3]
daandfmerged = pd.concat(frames)
daandfmerged = daandfmerged.sort_values(by=['SecondsFromStart'])

# Cumsum columns for graphing
daandfmerged['AntiPenalty1'] = daandfmerged['AntiPenalty1'].cumsum()
daandfmerged['AntiPenalty2'] = daandfmerged['AntiPenalty2'].cumsum()
daandfmerged['AntiPenalty3'] = daandfmerged['AntiPenalty3'].cumsum()

# Plotting
# x=daandfmerged["SecondsFromStart"]
# y1=daandfmerged['AntiPenalty1']
# y2=daandfmerged['AntiPenalty2']
# fig, ax = plt.subplots()
# ax.plot(x, [y1, y2])
# fig.set_size_inches(20, 10)
# plt.xlabel("Time (s)")
# plt.ylabel("Penalty *not* given")
# plt.show()

# Define x, y1, and y2
x_1 = daandfmerged["SecondsFromStart"]
y1_1=daandfmerged['AntiPenalty1']
y2_1=daandfmerged['AntiPenalty2']
y3_1=daandfmerged['AntiPenalty3']


# Interpolate missing values


# Create a stacked area plot with labels and legend
# plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()
ax.plot(x_1, y1_1, label='Run 1', linestyle='--', marker='.', markersize=5)
ax.plot(x_1, y2_1, label='Run 2 (unfinished)', linestyle='--', marker='x', markersize=5)
ax.plot(x_1, y3_1, label='Run 3', linestyle='--', marker='+', markersize=5)

# Set axis labels
plt.xlabel("Time (seconds) (Lower is better)")
plt.ylabel("Score achieved (StartScore - Penalty) (Higher is better)")

# Add legend and set figure size
plt.legend(loc='upper left')
fig.set_size_inches(10, 7.5)

# Show the plot
plt.show()

# %%
# Create a stacked area plot with labels and legend
# fig, ax = plt.subplots()
# ydelta_1 = y1_1 - y2_1
# ydelta_2 = y1_2 - y2_2
# ax.plot(x_1, ydelta_1, label='Plot 1')
# ax.plot(x_2, ydelta_2, label='Plot 2')
# fig.set_size_inches(20, 10)

# # Invert y-axis and set axis labels
# plt.xlabel("Time (s)")
# plt.ylabel("Penalty not given (Higher is better)")

# # Add legend
# plt.legend()

# # Show the plot
# plt.show()

# %%