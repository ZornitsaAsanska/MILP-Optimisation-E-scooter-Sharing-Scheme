'''
Converting location coordinates
from (eastings, northings) to (lat, long)
'''

import pandas as pd
import numpy as np
from convertbng.util import convert_lonlat
idx = [0, 3, 6, 9, 10, 12, 13, 14, 15, 16, 22, 28, 35, 36, 37, 41, 45, 46, 48, 49, 50, 51, 53, 55, 58, 59, 63, 64, 65,
       66, 67, 69, 70, 75, 76, 77, 78, 80, 82, 85, 86, 88, 92, 93, 94, 96, 98, 100, 102, 104, 105, 106, 107, 108, 109, 110]

df_coord = pd.read_csv("Data/Model Data - Coordinates.csv")
eastings = df_coord["Average of Easting"]
northings = df_coord["Average of Northing"]

list_lon_lat = convert_lonlat(eastings, northings)
list_lon_lat = np.array(list(zip(list_lon_lat[0], list_lon_lat[1])))
np.savetxt("Data/coordinates.csv", list_lon_lat, delimiter=',')

list_lon_lat_reduced = list_lon_lat[idx]
np.savetxt(f"Data/coordinates-{len(idx)}loc.csv", list_lon_lat_reduced, delimiter=',')