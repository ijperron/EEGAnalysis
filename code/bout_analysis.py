import pandas as pd
import numpy as np
import csv
import xlsxwriter
import re
from openpyxl import load_workbook
import os

def read_in_file(config_dict,filename):
    reader = csv.reader(open(os.path.join(config_dict['file_directory'], filename), "rt"))

    i = 0
    for row in reader:
        if len(row) == 0:
            continue   
        elif row[0] == 'EpochNo':
            break
        i+=1

    df = pd.read_csv(config_dict['file_directory'] + '/' + filename,skiprows = i+2,index_col='EpochNo')
    df = df.iloc[:, :-1]
    df['bout_num'] = (df.Stage.shift(1) != df.Stage).cumsum()

    return df

def switch_L_and_D(df, lights_off_zt):
    light = [x for x in df.ZT if int(x.split('-')[1]) <= lights_off_zt]
    dark = [x for x in df.ZT if int(x.split('-')[1]) > lights_off_zt]
    df['ZT'] = dark + light
    df = df.reindex(np.argsort([int(x.split('-')[1]) for x in dark+light])).reset_index(drop=True)
    
    return df

def get_stage_totals(df,
                     num_hours_per_segment_totals,
                     num_total_hours,
                     seconds_per_epoch,
                     lights_off_zt,
                     L_or_D_first):
    
    df_totals = pd.DataFrame()
    for i in np.arange(num_total_hours/num_hours_per_segment_totals):
        imin = int(i*num_hours_per_segment_totals*(3600/seconds_per_epoch))
        imax = int((i+1)*num_hours_per_segment_totals*(3600/seconds_per_epoch))
        z = 'ZT' + str(int(i*num_hours_per_segment_totals)) + '-' + str(int((i+1)*num_hours_per_segment_totals))

        dict_totals = {**{'epoch_min': imin, 'epoch_max': imax, 'ZT':z}, 
                       **(df.iloc[imin:imax].Stage.value_counts()*(seconds_per_epoch/60)).to_dict()}

        df_totals = df_totals.append(pd.DataFrame(dict_totals, index=[0]),ignore_index=True,sort=False)

    df_totals.fillna(0,inplace=True)
    
    if L_or_D_first == 'D':
        df_totals = switch_L_and_D(df_totals, lights_off_zt)
    
    return df_totals

def get_bout_agg(dfb):
    dfg = dfb.groupby('Stage').agg({'count','mean'})
    dfg.columns = ['_'.join(col).strip() for col in dfg.columns.values]
    return dfg.reset_index()

def get_bout_dist(dfb, dist_cutoffs,dist_labels):
    df_dist = pd.cut(dfb[dfb.Stage == 'W']['bout'], bins= dist_cutoffs + [np.inf], labels = dist_labels).value_counts().sort_index().to_frame()
    df_dist = df_dist.reset_index().rename(columns = {'index':'bout_dist_cat'})
    return df_dist

def get_bout_details(df, 
                     num_hours_per_segment_bouts,
                     num_total_hours,
                     seconds_per_epoch,
                     dist_cutoffs,
                     lights_off_zt,
                     L_or_D_first):
    
    df_bout_agg = pd.DataFrame()
    df_bout_dist = pd.DataFrame()
    for i in np.arange(num_total_hours/num_hours_per_segment_bouts):
        imin = int(i*num_hours_per_segment_bouts*(3600/seconds_per_epoch))
        imax = int((i+1)*num_hours_per_segment_bouts*(3600/seconds_per_epoch))
        
        dfb = (df[['Stage','bout_num']].iloc[imin:imax].reset_index().\
               groupby(['Stage','bout_num']).count() * seconds_per_epoch).\
                reset_index().drop("bout_num",axis=1).rename(columns={'EpochNo':'bout'})
        
        dfg = get_bout_agg(dfb)
        dfg['ZT'] = 'ZT' + str(int(i*num_hours_per_segment_bouts)) + '-' + str(int((i+1)*num_hours_per_segment_bouts))
        if L_or_D_first == 'D':
            dfg = switch_L_and_D(dfg,lights_off_zt)
        df_bout_agg = df_bout_agg.append(dfg,ignore_index=True,sort=False)
        
        dist_labels = [str(x) for x in dist_cutoffs[1:] + ['>' + str(dist_cutoffs[-1])]]
        dfd = get_bout_dist(dfb, dist_cutoffs, dist_labels)
        dfd['ZT'] = 'ZT' + str(int(i*num_hours_per_segment_bouts)) + '-' + str(int((i+1)*num_hours_per_segment_bouts))
        if L_or_D_first == 'D':
            dfd = switch_L_and_D(dfd, lights_off_zt)
        df_bout_dist = df_bout_dist.append(dfd,ignore_index=True,sort=False)
    
    if L_or_D_first == 'D':
        df_bout_agg = switch_L_and_D(df_bout_agg)
        df_bout_dist = switch_L_and_D(df_bout_dist)
    
    return df_bout_agg, df_bout_dist

def get_empty_frames():
    all_totals = pd.DataFrame()
    all_bouts = pd.DataFrame()
    all_bout_dist = pd.DataFrame()
    all_spectral = pd.DataFrame()
    
    return all_totals, all_bouts, all_bout_dist, all_spectral   

def run_analyses(config_dict, all_conditions, condition_cols):
    all_totals, all_bouts, all_bout_dist, all_spectral = get_empty_frames()
    
    for i in np.arange(all_conditions.shape[0]):
        print("Running analysis for ", all_conditions.loc[i].raw_filename)
        df = read_in_file(config_dict, all_conditions.loc[i].raw_filename)
    
        if config_dict['get_stage_totals'] == 'T':
            df_totals = get_stage_totals(df = df,
                         num_hours_per_segment_totals = config_dict['num_hours_per_segment_totals'],
                         num_total_hours = config_dict['num_total_hours'],
                         seconds_per_epoch = config_dict['seconds_per_epoch'],
                         lights_off_zt = config_dict['lights_off_zt'],
                         L_or_D_first = config_dict['L_or_D_first'])
            
            for col in condition_cols:
                df_totals[col] = all_conditions.iloc[i][col]

            all_totals = all_totals.append(df_totals,ignore_index=True,sort=False)
         
        if config_dict['get_bout_details'] == 'T':
            df_bouts, df_bout_dist = get_bout_details(df = df, 
                                        num_hours_per_segment_bouts = config_dict['num_hours_per_segment_bouts'],
                                        num_total_hours = config_dict['num_total_hours'],
                                        seconds_per_epoch = config_dict['seconds_per_epoch'],
                                        dist_cutoffs = config_dict['dist_cutoffs'],
                                        lights_off_zt = config_dict['lights_off_zt'],
                                        L_or_D_first = config_dict['L_or_D_first'])          
                  
            for col in condition_cols:
                df_bouts[col] = all_conditions.iloc[i][col]
                df_bout_dist[col] = all_conditions.iloc[i][col]
       
            all_bouts = all_bouts.append(df_bouts,ignore_index=True,sort=False)
            all_bout_dist = all_bout_dist.append(df_bout_dist,ignore_index=True,sort=False)       
    
    return all_totals, all_bouts, all_bout_dist, all_spectral

def sort_by_ZT(df, other_factors = []):
    df['int_vals'] = df.ZT.apply(lambda s: int(re.search('ZT(.*)-',s).group(1)))
    df.sort_values(['int_vals'] + other_factors,inplace=True)
    return df.iloc[:,:-1].set_index(['ZT'] + other_factors)

def write_to_excel(df, config_dict, condition_cols):
    custom_sort = {'W':0,'NR':1,'R':2}
    if df.empty is False:
        if df.name == 'all_totals':
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_all_totals.xlsx'
            book = pd.ExcelWriter(fileout, engine='openpyxl')
            for z in zip(['W','NR','R'],['Wake_totals','NREM_totals','REM_totals']):
                dft = pd.pivot_table(data = df, index = 'ZT',columns = condition_cols,values = z[0]).reset_index()
                dft = sort_by_ZT(dft)
                dft.to_excel(book,sheet_name = z[1],index=True)      
            book.save()
            book.close()
        elif df.name in ['all_bouts']:
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_bout_details.xlsx'
            book = pd.ExcelWriter(fileout, engine='openpyxl')
            for b in ['bout_count','bout_mean']:
                dft = pd.pivot_table(data = df, index = ['Stage','ZT'],columns = condition_cols,values = b).reset_index()
                dft['stage_sort_val'] = dft.Stage.map(custom_sort)
                dft = sort_by_ZT(dft,['stage_sort_val'])
                dft = dft.reset_index().set_index('ZT').iloc[:,1:]
                dft.to_excel(book,sheet_name = b,index=True)     
            book.save()
            book.close()
        elif df.name == 'all_bout_dist':
            fileout = config_dict['final_excel_output_name'].split('.')[0] + '_bout_details.xlsx'
            dft = pd.pivot_table(data = df, index = ['ZT','bout_dist_cat'],columns = condition_cols,values = 'bout').reset_index()
            dft = sort_by_ZT(dft,['bout_dist_cat'])
            
            with pd.ExcelWriter(fileout, engine = 'openpyxl', mode='a') as book:
                dft.to_excel(book, 'wake_bout_distrib', index=True)
            book.save()
            book.close()