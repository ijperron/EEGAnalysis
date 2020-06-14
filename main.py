import os, sys
sys.path.append(os.path.join(os.getcwd(), 'code'))

import numpy as np
import pandas as pd
from get_config import *
from get_animal_conditions import *
#from get_conditions import *
#from run_analysis import *
#from bout_analysis import *

def main():
    
    config_dict = read_in_config_file()   
    all_conditions = read_in_conditions_file(config_dict)
    
    print('test3')
    
if __name__ == "__main__":
    main()
    
    print("Completed")
    