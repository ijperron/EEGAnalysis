import os, sys
sys.path.append(os.path.join(os.getcwd(), 'code'))

import numpy as np
import pandas as pd
#from get_config import *
#from get_conditions import *
#from run_analysis import *
#from bout_analysis import *
from get_animal_conditions import *

def read_in_config_file():
    
    #Read in config.txt file
    config_path = os.path.join(os.getcwd(), 'required_config')
    print("Reading in config.txt file from location")
    print(config_path)
    
    response = input('Is this the correct config.txt file? (y/n)')
    for i in np.arange(5):
        if str.lower(response) == 'y':
            get_config(config_path)
            break
        elif str.lower(response) == 'n':
            print("Update config in that location and re-run")
            sys.exit(0)
        elif i+1 == 5:
            print("Maximum number of input tried exceeded. Quitting program...")
            sys.exit(0)
        else:
            response = input("Invalid input. Is this the correct config.txt file? (y/n)")
     
    
def main():
    
    read_in_config_file()
    create_conditions_file()
    
    print('test3')
    
if __name__ == "__main__":
    main()
    
    print("Completed")
    