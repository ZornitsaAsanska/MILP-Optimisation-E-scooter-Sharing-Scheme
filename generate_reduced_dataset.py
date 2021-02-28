'''
Extracting a small set of candidate locations
to run the model on
'''

import numpy as np
import pandas as pd
import os

# Selected reduced set of location (indices)
idx = [3,7,12,13,14,22,35,37,45,53,63,64,65,67,76,78,82,88,100,105]

demand = dict()
files = os.listdir('Data/Full Demand/')
for i, f in enumerate(files):
    hour = int(f.split(sep='.', maxsplit=1)[0])
    df = pd.read_csv('Data/Full Demand/' + f)
    # demand_arr = df.values[:-1,1:-1]
    demand[hour] = df

for k,v in demand.items():
    rows = v.loc[idx]
    locations = list(rows['Row Labels'])
    locations.insert(0,'Row Labels')
    reduced = rows[locations]
    csv = reduced.to_csv(index=False)
    with open('Data/Reduced set Demand/' + str(k) + '.csv', 'w') as f:
        f.write(csv)