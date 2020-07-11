import os
import sys
import numpy as np

def read_config(config_filename):
    config_dict = {}
    for l in open(config_filename, 'r') .readlines():
        if l[0] == '#':
            continue
        config_dict[l.split(' = ')[0]] = l.split(' = ')[1].split('\n')[0]
    
    for i in config_dict:
        if (config_dict[i][0] == '[') & (config_dict[i][-1] == ']'):
            config_dict[i] = [int(x) for x in config_dict[i][1:-1].split(',')]
            
        try: 
            config_dict[i] = int(config_dict[i])
        except:
            pass
        
    return config_dict

def create_config():    
    default_config = {'id_condition_filename': 'animal_conditions.csv',
                     'conditions_directory': os.getcwd(),
                     'final_excel_output_name': 'EEGAnalysis_output.xlsx',
                     'final_output_directory': os.getcwd(),
                     'file_directory': os.getcwd(),
                     'num_hours_per_segment_totals': 2,
                     'num_total_hours': 24,
                     'L_or_D_first': 'L',
                     'seconds_per_epoch': 4,
                     'lights_off_zt': 12,
                     'num_hours_per_segment_bouts': 12,
                     'dist_cutoffs': [0, 16, 32, 64, 128, 256, 512, 1024, 2048],
                     'num_epochs_per_segment': 225,
                     'get_stage_totals': 'T',
                     'get_bout_details': 'T',
                     'get_spectral': 'F'}
    
    f = open("config.txt","w")
    for k in default_config:
        f.write(str(k) + ' = ' + str(default_config.get(k)) + '\n')
    
    f.close()