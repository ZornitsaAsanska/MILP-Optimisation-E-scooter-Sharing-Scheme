'''
Extracting a small set of candidate locations
to run the model on
'''

import numpy as np
import pandas as pd
import os

# Selected reduced set of location (indices)
idx = [0, 3, 6, 9, 10, 12, 13, 14, 15, 16, 22, 28, 35, 36, 37, 41, 45, 46, 48, 49, 50, 51, 53, 55, 58, 59, 63, 64, 65,
       66, 67, 69, 70, 75, 76, 77, 78, 80, 82, 85, 86, 88, 92, 93, 94, 96, 98, 100, 102, 104, 105, 106, 107, 108, 109, 110]

demand = dict()
files = os.listdir('Data/Full Demand/')
for i, f in enumerate(files):
    hour = int(f.split(sep='.', maxsplit=1)[0])
    df = pd.read_csv('Data/Full Demand/' + f)
    # demand_arr = df.values[:-1,1:-1]
    demand[hour] = df

for k, v in demand.items():
    rows = v.loc[idx]
    locations = list(rows['Row Labels'])
    locations.insert(0, 'Row Labels')
    reduced = rows[locations]
    csv = reduced.to_csv(index=False)
    with open('Data/Final set Demand/' + str(k) + '.csv', 'w') as f:
        f.write(csv)

# Distance Data
df_distance = pd.read_csv("Data/Model Data - Distance Matrix.csv")
df_distance.fillna(0, inplace=True)

rows = df_distance.loc[idx]
locations = list(rows['Location'])
locations.insert(0, 'Location')
reduced = rows[locations]
csv = reduced.to_csv(index=False)
with open('Data/Model Data - 56loc Distance.csv', 'w') as f:
    f.write(csv)

# Penalty data
df_penalty = pd.read_csv("Data/Penalty Carbon Costs.csv")
C_pen_reduced = df_penalty.loc[idx]
csv = C_pen_reduced.to_csv(index=False)
with open('Data/Penalty Carbon Costs 56loc.csv', 'w') as f:
    f.write(csv)
