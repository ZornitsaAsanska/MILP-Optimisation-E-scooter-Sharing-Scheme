'''
Converting location coordinates
from (eastings, northings) to (lat, long)
'''

import pandas as pd
import numpy as np
from convertbng.util import convert_lonlat

df_coord = pd.read_csv("Model Data - Coordinates.csv")
eastings = df_coord["Average of Easting"]
northings = df_coord["Average of Northing"]

list_lon_lat = convert_lonlat(eastings, northings)
list_lon_lat = np.array(list(zip(list_lon_lat[0], list_lon_lat[1])))
np.savetxt("Data/coordinates.csv", list_lon_lat, delimiter=',')