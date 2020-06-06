def main():
    import pandas as pd
    import os
    
    config_dict = {}
    for l in open('config.txt', 'r') .readlines():
        if l[0] == '#':
            continue
        
        config_dict[l.split(' = ')[0]] = l.split(' = ')[1].split('\n')[0]

    animal_conditions = pd.DataFrame()

    for f in os.listdir(config_dict['file_directory']):
        if (f.split('.')[1] == 'csv') & (f != config_dict['id_condition_filename']):
            print(f)

            dict_ac = {'raw_filename':f,
                       'animal_id':f.split('_')[0],
                       'sleep_condition':f.split('_')[1],
                       'experimental_condition':f.split('_')[2].split('.')[0]
                      }

            animal_conditions = animal_conditions.append(pd.DataFrame(dict_ac,index=[0]),ignore_index=True, sort=False)

    animal_conditions.to_csv(config_dict['id_condition_filename'],index=False)
    
if __name__ == "__main__":
    main()