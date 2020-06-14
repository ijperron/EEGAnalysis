import os
import sys

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

def read_in_config_file():
    config_filename = 'config.txt'
    
    #Read in config.txt file  
    if config_filename in os.listdir():
        print("Found config.txt in current directory...")
        return read_config(config_filename)
    else:
        response = input("No config.txt in current directory. Would you like to create a new one? (y/n")
        for i in np.arange(5):
            if str.lower(response) == 'y':
                create_config()
                print("config.txt file created. Check settings and re-run.")
                sys.exit(0)
            elif str.lower(response) == 'n':
                print("Change directory to location with correct config.txt file and re-run.")
                sys.exit(0)
            elif i+1 == 5:
                print("Maximum number of input tried exceeded. Quitting program...")
                sys.exit(0)
            else:
                response = input("Invalid input. Would you like to create config.txt file? (y/n)")

def create_config():    
    default_config = {'id_condition_filename': 'animal_conditions.csv',
                     'conditions_directory': os.getcwd(),
                     'final_excel_output_name': 'ip_test_output.xlsx',
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
            
    return default_config