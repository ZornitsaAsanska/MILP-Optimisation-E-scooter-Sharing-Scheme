import pandas as pd
import numpy as np
import itertools
import argparse
import os
from pulp import *

parser = argparse.ArgumentParser(description="E-scooter Sharing Scheme - Optimisation Model")
parser.add_argument('--reduced', action = 'store_true', help="A reduced dataset is used for faster computation")
args = parser.parse_args()

problem = LpProblem("E-Scooter Allocation", LpMinimize)

if args.reduced:
    df_distance = pd.read_csv("Data/Model Data - Smaller set Distance.csv")
else:
    df_distance = pd.read_csv("Data/Model Data - Distance Matrix.csv")

df_distance.fillna(0, inplace=True)
distance = df_distance.values[:,1:]
distance_dict = { (x,y): distance[x][y] for x in range(distance.shape[0]) for y in range(distance.shape[1])}

locations = list(df_distance['Location'])
location_idx = np.arange(0, len(locations))
loc_count = len(locations)
print(locations)
if args.reduced:
    path = 'Data/Reduced set Demand/'
else:
    path = 'Data/Full Demand/'

demand = dict()
files = os.listdir(path)
for f in files:
    hour = int(f.split(sep='.', maxsplit=1)[0])
    df = pd.read_csv(path + f)
    if args.reduced:
        demand_arr = df.values[:,1:]
        demand[hour] = demand_arr
    else:
        # Removing Grand Total values as end row and end column
        demand_arr = df.values[:-1,1:-1]
        demand[hour] = demand_arr

demand_dict = dict()
for i,(_,v) in enumerate(demand.items()):
    demand_dict.update({(x,y,i): v[x][y] for x in range(loc_count) for y in range(loc_count)})
# Parameters
M = sys.maxsize
if args.reduced:
    Nmax = 10
    Smax = 20
else:
    Nmax = 40
    Smax = 20

# Cost values
C_scooter_km = 7
C_fixed_scooter = 167
C_fixed_dock = 46
C_fixed_station = 6
# Cost relocation
C_r = 160

# Penalty
if args.reduced:
    df_penalty = pd.read_csv("Data/Penalty Carbon Costs Smaller set.csv")
    C_pen = df_penalty.values[:, 1]
else:
    df_penalty = pd.read_csv("Data/Penalty Carbon Costs.csv")
    C_pen = df_penalty.values[:-1, 1]

# Sets
T = np.arange(0,len(files))
# each location at a given time
X = list(itertools.product(location_idx, T))
A1 = [(xi, xj) for xi in X for xj in X if xi[0] != xj[0] and xi[1]+1==xj[1]]
A2 = [(xi, xj) for xi in X for xj in X if xi[0]==xj[0] and xi[1]+1==xj[1]]
# Relocation
A3 = [(xi, xj) for xi in X for xj in X if xi[0]!=xj[0] and xi[1]==T[-1] and xj[1]==T[0]]

# Decision Variables
Yi = LpVariable.dicts("Station Presence", location_idx,0,cat=const.LpBinary)
Zi = LpVariable.dicts("Size", location_idx, 0, cat="Continuous")
# Relocation
Rij = LpVariable.dicts("#Relocated_Scooters", A3, 0, cat=const.LpInteger)
Vit = LpVariable.dicts("#Available_Scooters",X,0,cat="Continuous")
Sit = LpVariable.dicts("#Stocked_Scooters", A2, 0, cat="Continuous")
Ditj = LpVariable.dicts("#Used_Scooters", A1, 0 ,cat="Continuous")

# Objective function
problem+=lpSum(Ditj[((i,ti),(j,tj))]*distance_dict[(i,j)]*C_scooter_km for ((i,ti),(j,tj)) in A1) + \
    lpSum((demand_dict[(i,j,ti)]-Ditj[((i,ti),(j,tj))])*distance_dict[(i,j)]*C_pen[i] for ((i,ti),(j,tj)) in A1) + \
    lpSum(Rij[((i,ti), (j,tj))]*distance_dict[(i,j)]*C_r for ((i,ti), (j,tj)) in A3) + \
    lpSum(Vit[(i,t)]*C_fixed_scooter for (i,t) in X if t==0) + \
    lpSum(Zi[i]*C_fixed_dock for i in location_idx) + \
    lpSum(Yi[i]*C_fixed_station for i in location_idx), "Objective function"

# Constraints
for (i,ti) in X:
    if ti !=0:
        problem+= Vit[(i,ti-1)] - lpSum(Ditj[((i,ti-1),(j,tj))] for (j,tj) in X if tj==ti and i !=j) + lpSum(Ditj[((j, tj),(i, ti))] for (j,tj) in X if tj == ti-1 and i !=j) == Vit[(i,ti)], f"Availability Balance {(i,ti)}"

for (i,ti) in X:
    if ti!=T[-1]:
        problem+=Vit[(i,ti)] - lpSum(Ditj[((i,ti),(j,tj))]for (j,tj) in X if i !=j and ti+1==tj) == Sit[((i,ti), (i,ti+1))], f"Stocked Scooters for {(i,ti)}"

# Relocation constraint
for i in location_idx:
    problem+=Vit[(i,0)] == Vit[(i,T[-1])] + lpSum(Rij[((j,T[-1]), (i,0))] for j in location_idx if i!=j) - lpSum(Rij[((i,T[-1]), (j,0))] for j in location_idx if i!=j), f"Relocation balance for location {i}"

for i in location_idx:
    problem+=lpSum(Rij[((i,T[-1]), (j,0))] for j in location_idx if i!=j) <= Vit[(i,T[-1])], f"Relocation availability for location {i}"

for (i,ti) in X:
    problem+= Zi[i] >=Vit[(i,ti)], f"Size constraint for {(i,ti)}"

for (i,ti) in X:
    problem+=Vit[(i,ti)] <= M*Yi[i], f"Availability against Dock present{(i,ti)}"

for i in location_idx:
    problem+=Yi[i] <= Zi[i], f"Size constraint for {i}"

for ((i,ti),(j,tj)) in A1:
    problem+=Ditj[((i,ti),(j,tj))]<=demand_dict[(i,j,ti)], f"Maximum Demand for {((i,ti),(j,tj))}"

for i in location_idx:
    problem+=Zi[i] <= Smax, f"Maximum size for {i}"

problem+=lpSum(Yi[i] for i in location_idx) <= Nmax, f"Maximum number of docks"

problem.writeLP("E-scooterProblem.lp")
problem.solve()
print('Problem Status: ' + str(LpStatus[problem.status]))
print('Objective value: ' + str(value(problem.objective)))

for v in problem.variables():
    if v.varValue>0:
        print(v.name, "=", v.varValue)

# Extracting the results
#(idx, LpVariable)
size_list = []
for _,v in Zi.items():
    size_list.append(v.value())

station_list = []
for _,v in Yi.items():
    station_list.append(v.value())

df_results = pd.DataFrame(list(zip(locations, station_list, size_list)), columns=["Location","Station", "Size"])
#df_results.head()

df_results.to_csv("results3.csv", index=False)

for k, v in Sit.items():
    print(str(k[0]) + ', '+ str(k[1]) + "=" + str(v.varValue))

total_Sit = dict()
for k,v in Sit.items():
    if k[0][1] not in total_Sit:
        total_Sit[k[0][1]] = int(v.varValue)
    else:
        total_Sit[k[0][1]]+=int(v.varValue)

# Sum(Vit[i][0]) over all locations i - the total number of scooters
total_Vit = dict()
for k,v in Vit.items():
    if k[1] not in total_Vit:
        total_Vit[k[1]] = int(v.varValue)
    else:
        total_Vit[k[1]]+=int(v.varValue)
