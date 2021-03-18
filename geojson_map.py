'''
Generating a GeoJson map
E-scooter Depot Location and Size
'''

import numpy as np
import pandas as pd
import argparse
from geojson import Feature, Point, FeatureCollection, dump, dumps

parser = argparse.ArgumentParser()
parser.add_argument("coordinatePath", help="Generate a geojson map using the reduced set of data points")
parser.add_argument("modelPath", help="Path to the results of the optimisation model")

args = parser.parse_args()

# Reading results of the Optimisation model into a dataframe
# along with (lat, lon) coordinates of each candidate location
df_locations = pd.read_csv(args.modelPath)
coords = np.loadtxt(args.coordinatePath, delimiter=",")

df_locations['Longitude'] = coords[:,0]
df_locations['Latitude'] = coords[:,1]

# List of GeoJson Feature Objects
features = list()
for idx, row in df_locations.iterrows():
    point = Point((row['Longitude'], row['Latitude']))
    if int(row['Station']):
        properties = {"Name": row['Location'], "Depot": 'Yes', "Docks": row['Size'], "marker-color": "#008000", "marker-symbol": "scooter"}
         
    else:
        properties = {"Name": row['Location'], "Depot": 'No', "marker-color": "#FF0000", "marker-symbol": "cross","marker-size": "small"}
    
    feature = Feature(geometry=point, properties = properties)
    features.append(feature)

# Generating FeatureCollection object and .geojson file 
feature_collection = FeatureCollection(features)
json_str = dumps(feature_collection, separators=(',', ':'))

if args.reduced:
    with open('E-scooter stations-reduced.geojson', 'w') as f:
        f.write(json_str)
else:
    with open('E-scooter stations.geojson', 'w') as f:
        f.write(json_str)