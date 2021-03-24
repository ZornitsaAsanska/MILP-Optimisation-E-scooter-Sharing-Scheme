import os
import pandas as pd
import numpy as np


class Report():

    def __init__(self, fname, modelName, loc, minimize=True) -> None:
        self.fname = fname
        self.modelName = modelName
        self.loc = loc
        self.minimize = minimize
        try:
            os.mkdir(modelName)
        except OSError:
            print(f"Could not create directory {modelName}. It probably already exists")

def station_stats(trips: dict):
    with pd.ExcelWriter('Station statistics_NOcuts.xlsx') as writer1:
        for k in trips.keys():
            trips[k].to_excel(writer1, sheet_name=k, index=False)

            

