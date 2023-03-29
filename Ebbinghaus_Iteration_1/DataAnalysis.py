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
pathExtension = "Ebbinghaus_Iteration_1"
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
# Loading new DF for run_ run_s with search
run_df = newdata
run_df1 = run_df[run_df['GameSessionId'].str.contains('Run_Daan1')]
run_df2 = run_df[run_df['GameSessionId'].str.contains('Run_Daan2')]
run_df3 = run_df[run_df['GameSessionId'].str.contains('Run_Daan3')]

# Apply the function to the time column in your DataFrame
run_df1['SecondsFromStart'] = run_df1['StopTime'].apply(to_epoch)
run_df1['SecondsFromStart'] = run_df1['SecondsFromStart'] - run_df1['SecondsFromStart'].iloc[0]
run_df2['SecondsFromStart'] = run_df2['StopTime'].apply(to_epoch)
run_df2['SecondsFromStart'] = run_df2['SecondsFromStart'] - run_df2['SecondsFromStart'].iloc[0] 
run_df3['SecondsFromStart'] = run_df3['StopTime'].apply(to_epoch)
run_df3['SecondsFromStart'] = run_df3['SecondsFromStart'] - run_df3['SecondsFromStart'].iloc[0] 


# Filter by columns that have scoring
run_df1 = run_df1.query("`StartScore` >= 1")
run_df2 = run_df2.query("`StartScore` >= 1")
run_df3 = run_df3.query("`StartScore` >= 1")

# New column for graphing with penalty delta
run_df1['AntiPenalty1'] = run_df1['StartScore'] - run_df1['Penalty']
run_df2['AntiPenalty2'] = run_df2['StartScore'] - run_df2['Penalty']
run_df3['AntiPenalty3'] = run_df3['StartScore'] - run_df3['Penalty']


# Merging dfs
frames = [run_df1, run_df2, run_df3]
run_dfmerged = pd.concat(frames)
run_dfmerged = run_dfmerged.sort_values(by=['SecondsFromStart'])

# Cumsum columns for graphing
run_dfmerged['AntiPenalty1'] = run_dfmerged['AntiPenalty1'].cumsum()
run_dfmerged['AntiPenalty2'] = run_dfmerged['AntiPenalty2'].cumsum()
run_dfmerged['AntiPenalty3'] = run_dfmerged['AntiPenalty3'].cumsum()

# Plotting
# x=run_dfmerged["SecondsFromStart"]
# y1=run_dfmerged['AntiPenalty1']
# y2=run_dfmerged['AntiPenalty2']
# fig, ax = plt.subplots()
# ax.plot(x, [y1, y2])
# fig.set_size_inches(20, 10)
# plt.xlabel("Time (s)")
# plt.ylabel("Penalty *not* given")
# plt.show()

# Define x, y1, and y2
x_1 = run_dfmerged["SecondsFromStart"]
y1_1=run_dfmerged['AntiPenalty1']
y2_1=run_dfmerged['AntiPenalty2']
y3_1=run_dfmerged['AntiPenalty3']


# Interpolate missing values


# Create a stacked area plot with labels and legend
# plt.style.use('_mpl-gallery')
fig, ax = plt.subplots()
ax.plot(x_1, y1_1, label='run_ 1', linestyle='--', marker='.', markersize=5)
ax.plot(x_1, y2_1, label='run_ 2 (unfinished)', linestyle='--', marker='x', markersize=5)
ax.plot(x_1, y3_1, label='run_ 3', linestyle='--', marker='+', markersize=5)

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