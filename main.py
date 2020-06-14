import os, sys
sys.path.append(os.path.join(os.getcwd(), 'code'))

import numpy as np
import pandas as pd
import datetime as dt
from get_config import *
from get_animal_conditions import *
from bout_analysis import *

def main():  
    config_dict = read_in_config_file()   
    all_conditions = read_in_conditions_file(config_dict)
    
    condition_cols = []
    for col in all_conditions.columns:
        if col not in ['raw_filename']:
            condition_cols.append(col)
    
    all_totals, all_bouts, all_bout_dist, all_spectral = run_analyses(config_dict, all_conditions, condition_cols)
    all_totals.name = 'all_totals'
    all_bouts.name = 'all_bouts'
    all_bout_dist.name = 'all_bout_dist'
    all_spectral.name = 'all_spectral'
    
    for df in (all_totals, all_bouts, all_bout_dist, all_spectral):
        write_to_excel(df, config_dict)
    
if __name__ == "__main__":
    start_time = dt.datetime.now()
    main()
    end_time = dt.datetime.now()
    print("Completed, total time: {} seconds".format((end_time - start_time)/dt.timedelta(seconds=1))
    