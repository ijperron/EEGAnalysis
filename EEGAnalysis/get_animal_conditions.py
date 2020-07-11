import os
import sys
import pandas as pd
import numpy as np

def create_conditions(filedir,condname):
    animal_conditions = pd.DataFrame()
    for f in os.listdir(filedir):

        if (f.split('.')[1] == 'csv') & (f != condname):
            print("Data file read in: {}".format(f))

            dict_ac = {'raw_filename':f,
                       'animal_id':f.split('_')[0],
                       'sleep_condition':f.split('_')[1],
                       'experimental_condition':f.split('_')[2].split('.')[0]
                      }

            animal_conditions = animal_conditions.append(pd.DataFrame(dict_ac,index=[0]),ignore_index=True, sort=False)
            
    animal_conditions.to_csv(condname,index=False)