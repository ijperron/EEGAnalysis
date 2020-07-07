import os
import sys
import pandas as pd
import numpy as np

def create_conditions(filedir,condname):
    animal_conditions = pd.DataFrame()
    print(filedir)
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
    
    return print("{} file created. Check settings and re-run.".format(condname))

def read_in_conditions_file(config_dict):
    
    fname = config_dict['id_condition_filename']
    fdir = config_dict['conditions_directory']
    
    print("Looking for {} in location...".format(fname))
    
    if fname in os.listdir(fdir):
        all_conditions = pd.read_csv(os.path.join(fdir,fname))
        return all_conditions
    else:
        response = input("No {} in specified directory. Would you like to create a new one? (y/n)".format(fname))
        for i in np.arange(5):
            if str.lower(response) == 'y':
                create_conditions(config_dict['conditions_directory'],fname)          
                sys.exit(0)
            elif str.lower(response) == 'n':
                print("Place correct {} file in specified location and re-run.")
                sys.exit(0)
            elif i+1 == 5:
                print("Maximum number of input tried exceeded. Quitting program...")
                sys.exit(0)
            else:
                response = input("Invalid input. Would you like to create {} file? (y/n)".format(fname))
                            
