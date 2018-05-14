##### Import functions
import numpy as np
import pandas as pd

#### Define custom functions
def time_in_each_state(df,n_bins,num_hours,light_then_dark=True,unit_time='S'):
    #For easy amendment to relevant column names

    epoch_no = 'Epoch No.'
    count = 'Count'
    
    #Check to make sure the number of bins are even
    if n_bins % 2 != 0:
        return print('Number of bins must be an even number')
    
    #Declare empty arrays to be filled
    time_w = np.array([])
    time_n = np.array([])
    time_r = np.array([])
    
    #Step or bin size
    step_size = num_hours/n_bins

    for i in np.arange(0,num_hours,step_size):
        tmin = 900*i
        tmax = 900*(i+step_size)
        
        #Read only the portion of interest into temp dataframe
        df_temp = df[(df[epoch_no] >= tmin) & (df[epoch_no] < tmax)]
        
        #The temp file may be empty if the entire timespan is one epoch. Check for this and impute if necessary
        if df_temp.empty == True:
            df_temp = df[df[epoch_no] < tmax].iloc[[-1]]
            df_temp.Count = 900*step_size
        else:
            first_epoch = df_temp.iloc[0][epoch_no]
            if tmin != first_epoch:
                prev_row = df.iloc[[df_temp.index[0] - 2]]
                df_temp = pd.concat([prev_row, df_temp])
                df_temp = df_temp.set_value(index = df_temp.index[0], col = count, value = (first_epoch - tmin))

            last_epoch = df_temp.iloc[-1][epoch_no]
            if tmax != last_epoch: 
                df_temp = df_temp.set_value(index = df_temp.index[-1], col = count, value = (tmax - last_epoch))

        #Append to array, holding times in each state (w=wake, n=nrem, r=rem)
        time_w = np.append(time_w, df_temp[df_temp.Episode.str.contains('W') == True][count].sum())
        time_n = np.append(time_n, df_temp[df_temp.Episode.str.contains('N') == True][count].sum())
        time_r = np.append(time_r, df_temp[df_temp.Episode.str.contains('R') == True][count].sum())
        
    #Convert to pd DataFrame
    tot_times = pd.DataFrame(np.transpose([time_w,time_n,time_r]),columns = ['Wake_Time','NREM_Time','REM_Time'])
    
    #If file is 7pm - 7pm, then it will flip the array. That way all files are 7a - 7a. Default is True
    if light_then_dark == False:
        df_light = tot_times[int(n_bins/2):].copy()
        df_dark = tot_times[:int(n_bins/2)].copy()

        tot_times = pd.DataFrame()
        tot_times = pd.concat([df_light,df_dark]).reset_index(drop=True)
    
    #Can specify units of M=minutes or H=hours. Default is S=seconds
    if unit_time == "M":
        tot_times = tot_times/60
    elif unit_time == "H":
        tot_times = tot_times/3600
    
    #Return dataframe in time unit of choice. Default is seconds (4 second epochs)
    return 4*tot_times


def bout_architecture(df,n_bins,num_hours): 
    step_size = num_hours/n_bins
    num_total = np.array([])
    len_total = np.array([])
    cols = []
    
    if num_hours % n_bins != 0:
        return print('Invalid options: n_bins must be evenly divisible into num_hours')
    
    for i in list(['W','N','R']):
        df_sub = df[df.Episode.str.contains(i) == True][[epoch_no, dur]]

        num_total = np.append(num_total,df_sub[dur].count())
        len_total = np.append(len_total,df_sub[dur].mean())
        cols.append(i+ '_Total')
        
        if n_bins > 1:   
            for j in np.arange(0,num_hours,step_size):
                tmin = 900*j
                tmax = 900*(j+step_size)

                df_sub_temp = df_sub[(df_sub[epoch_no] >= tmin) & (df_sub[epoch_no] < tmax)]

                cols.append(i + '_' + str(int(j)) + '-' + str(int(j+step_size)))
                num_total = np.append(num_total,df_sub_temp[dur].count())
                len_total = np.append(len_total,df_sub_temp[dur].mean())
        
    df_out = pd.DataFrame(data = [num_total,len_total], columns = cols, index = ['Number','Length']).transpose()
    
    return df_out
    
