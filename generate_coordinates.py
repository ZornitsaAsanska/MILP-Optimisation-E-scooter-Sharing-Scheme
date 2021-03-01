'''
Converting location coordinates
from (eastings, northings) to (lat, long)
'''

import pandas as pd
import numpy as np
from convertbng.util import convert_lonlat

idx = [3,7,12,13,14,22,35,37,45,53,63,64,65,67,76,78,82,88,100,105]

df_coord = pd.read_csv("Data/Model Data - Coordinates.csv")
eastings = df_coord["Average of Easting"]
northings = df_coord["Average of Northing"]

list_lon_lat = convert_lonlat(eastings, northings)
list_lon_lat = np.array(list(zip(list_lon_lat[0], list_lon_lat[1])))
np.savetxt("Data/coordinates.csv", list_lon_lat, delimiter=',')

list_lon_lat_reduced = list_lon_lat[idx]
np.savetxt("Data/coordinates-reduced.csv", list_lon_lat_reduced, delimiter=',')