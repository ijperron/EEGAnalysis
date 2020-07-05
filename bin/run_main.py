#!/usr/bin/env python

import numpy as np
import pandas as pd
import datetime as dt
from EEGAnalysis.code.get_config import *
from EEGAnalysis.code.get_animal_conditions import *
from EEGAnalysis.code.bout_analysis import *

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
        write_to_excel(df, config_dict, condition_cols)
    