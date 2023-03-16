# %%
import os
import json
import pandas as pd
import pm4py
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
from pm4py.algo.simulation.montecarlo import algorithm as montecarlo_simulation
from pm4py.algo.conformance.tokenreplay.algorithm import Variants

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


SSRandy = newdata
SSRandy = SSRandy[SSRandy['GameSessionId'].str.contains('test')]
log = pm4py.read_xes("Data/test.xes")
log = pm4py.convert_to_event_log(log)
all_case_durations1 = pm4py.get_all_case_durations(log)
print(all_case_durations1)
# Convert the dataframe to an event log in XES format
dataframe = pm4py.format_dataframe(SSRandy, case_id='Sequence', activity_key='StepName', timestamp_key='StopTime')
event_log = pm4py.convert_to_event_log(dataframe)
all_case_durations = pm4py.get_all_case_durations(event_log)
print(all_case_durations)

pm4py.view_dfg(dfg, start_activities, end_activities)
map = pm4py.discover_heuristics_net(log)
pm4py.view_heuristics_net(map)
tree = pm4py.discover_process_tree_inductive(log)
pm4py.view_process_tree(tree)
# Apply the alpha miner algorithm to discover the process model
net, initial_marking, final_marking = pm4py.discover_petri_net_alpha(event_log)

process_model = pm4py.discover_bpmn_inductive(log)
pm4py.view_bpmn(process_model)