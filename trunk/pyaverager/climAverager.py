import time
import numpy as np
import rover
import climFileIO
from numpy import ma as MA

def avg_var(var,years,hist_dict,ave_info,file_dict,ave_type,timer,depend):

    '''
    Computes the average of a variable

    @param var         The name of the variable that is being  averaged.

    @param years       A list of the years that are in this average

    @param hist_dict   A dictionary that holds file references for all years/months. 

    @param ave_info    A dictionary of the type of average that is to be done.
                       Includes:  type, months_to_average, fn, and weights
                       (weights are not used in this function/average)
    
    @param file_dict   A dictionary which holds file pointers to the input files that
                       are needed by this average calculation.

    @param ave_type    The average type key that indicated which type of average will be done.

    @param timer       The timer class used for time bookkeeping.

    @param depend      Boolean variable to indicate if this average will be computed from previously calculated files. 
 
    @return var_Ave    The averaged results for this variable across the designated time frame.
    '''
    print('Computing ',ave_info['type'],' for ',var," for ",years)

    timer.start("Time to compute Average")

    # Get a sample month/file to look into to see if the variable contains missing values 
    #sample_month = next(iter(file_dict.values()).next().itervalues())
    sample_month = file_dict[years[0]][ave_info['months_to_average'][0]]

    # If the variable has missing values, we need to calculate the average
    # with a mask accumulator
    if hasattr(sample_month['fp'].variables[var],'_FillValue'):
        fillValue = getattr(sample_month['fp'].variables[var],'_FillValue')
        var_Ave = avg_var_missing(var,years,hist_dict,ave_info,file_dict,ave_type,fillValue,timer,depend)
    else:
        # Create average by creating a running sum and then divide by the count
        count = 0
        first = True
        for yr in years:
            for m in ave_info['months_to_average']:
            # Check if doing a winter average and get the correct year to pull
                if ((ave_type == 'djf' and depend == False) or ave_type == 'next_jan' 
		    or ave_type == 'next_feb' or ave_type == 'prev_dec'):
                    pull_year = climFileIO.which_winter_year(hist_dict, m, yr, years[0])
                else:
                    pull_year = yr
                timer.start("Variable fetch time")
                var_val = rover.fetch_slice(hist_dict,pull_year,m,var,file_dict)
                timer.stop("Variable fetch time")
                # Add the variable value to the accumulator
                if (first):
                    var_sum = var_val
                    first = False
                else:
                    var_sum = var_val + var_sum
                count+=1
        var_Ave = np.divide(var_sum,count)

    timer.stop("Time to compute Average")

    return var_Ave

def avg_var_missing(var,years,hist_dict,ave_info,file_dict,ave_type,fillValue,timer,depend):

    '''
    Computes the average of a variable that contains missing values

    @param var         The name of the variable that is being  averaged.

    @param years       A list of the years that are in this average

    @param hist_dict   A dictionary that holds file references for all years/months. 

    @param ave_info    A dictionary of the type of average that is to be done.
                       Includes:  type, months_to_average, fn, and weights
                       (weights are not used in this function/average)
    
    @param file_dict   A dictionary which holds file pointers to the input files that
                       are needed by this average calculation.

    @param ave_type    The average type key that indicated which type of average will be done.

    @param fillValue   The value that indicates missing values within the data.

    @param timer       The timer class used for time bookkeeping.

    @param depend      Boolean variable to indicate if this average will be computed from previously calculated files.

    @return var_Ave    The averaged results for this variable across the designated time frame.
    '''
    # if variable contains missing values, create a mask accumulator that will count how many masked values not to add & divide
    count = 0
    first = True
    fetch_time = 0

    first_mask = True
    for yr in years:
        for m in ave_info['months_to_average']:
            timer.start("Variable fetch time")
            # Check if doing a winter average and get the correct year to pull
            if ((ave_type == 'djf' and depend == False) or ave_type == 'next_jan'
                    or ave_type == 'next_feb' or ave_type == 'prev_dec'):
                pull_year = climFileIO.which_winter_year(hist_dict, m, yr,years[0])
            else:
                pull_year = yr
            var_val = rover.fetch_slice(hist_dict,pull_year,m,var,file_dict)
            timer.stop("Variable fetch time")
            var_filled = var_val.filled(fill_value=0) # zero out the masked grid points
            # Get and add mask values to the mask accumulator
            if (first_mask):
                if (MA.any(MA.getmask(var_val))):
                    mask_sum = (MA.getmask(var_val)).astype(int)
                    first_mask = False
            else:
                if (MA.any(MA.getmask(var_val))):
                    mask_sum = mask_sum + (MA.getmask(var_val)).astype(int)
            # Add the variable value accumulator using the filled, zeroed about values. 
            if (first):
                var_sum = var_filled
                first = False
            else:
                var_sum = var_filled + var_sum
            count+=1
    # Create an inverserse of the mask to divide by
    if (first_mask == True):
        inv = count
    else:
        inv = (count - mask_sum)
    # Divide by mask to get average
    np.seterr(divide='ignore', invalid='ignore')
    var_Ave = var_sum / inv
    # Replace any nan values with the fill value.  Nans will occur if there is a 
    # missing value for that array element in all slices that are averaged (ie. land in ocean files).
    if var_Ave.shape:
        var_Ave[np.isnan(var_Ave)]=fillValue
    else:
        print var,var_Ave

    return var_Ave

def weighted_avg_var(var,years,hist_dict,ave_info,file_dict,ave_type,timer,depend):

    '''
    Computes the weighted average of a variable

    @param var         The name of the variable that is being  averaged.

    @param years       A list of the years that are in this average

    @param hist_dict   A dictionary that holds file references for all years/months. 

    @param ave_info    A dictionary of the type of average that is to be done.
                       Includes:  type, months_to_average, fn, and weights
                       (weights are not used in this function/average)
    
    @param file_dict   A dictionary which holds file pointers to the input files that
                       are needed by this average calculation.

    @param ave_type    The average type key that indicated which type of average will be done.

    @param timer       The timer class used for time bookkeeping.

    @param depend      Boolean variable to indicate if this average will be computed from previously calculated files.

    @return var_Ave    The averaged results for this variable across the designated time frame.
    '''
    print('Computing weighted ',ave_info['type'],' for ',var," for ",years)

    timer.start("Time to compute Average")

    count = 0
    first = True

    # Create the sum of all slices
    sample_month = next(iter(file_dict.values()).next().itervalues())
    sample_fn = hist_dict[years[0]][0]['fn']

    # If the variable has missing values, we need to calculate the average differently
    if hasattr(sample_month['fp'].variables[var],'_FillValue'):
        fillValue = getattr(sample_month['fp'].variables[var],'_FillValue')
        var_Ave = weighted_avg_var_missing(var,years,hist_dict,ave_info,file_dict,ave_type,fillValue,timer,depend)
    else:
 
        # Create the sum of all slices
        for yr in years:
            i = 0
            for m in ave_info['months_to_average']:
                timer.start("Variable fetch time") 
                # Check if doing a winter average and get the correct year to pull
                if ((ave_type == 'djf' and depend == False) or ave_type == 'next_jan'
                    or ave_type == 'next_feb' or ave_type == 'prev_dec'):
                    pull_year = climFileIO.which_winter_year(hist_dict, m, yr,years[0])
                else:
                    pull_year = yr
                var_val = rover.fetch_slice(hist_dict,pull_year,m,var,file_dict)
                timer.stop("Variable fetch time")
                if (first):
                    var_sum = (var_val*ave_info['weights'][i])
                    first = False
                else:
                    var_sum = (var_val*ave_info['weights'][i]) + var_sum
                i+=1
            count+=1
        # Since the weights are only for 1 year, divide by total number of years
        var_Ave = np.divide(var_sum,count)

    timer.stop("Time to compute Average")

    return var_Ave

def weighted_avg_var_missing(var,years,hist_dict,ave_info,file_dict,ave_type,fillValue,timer,depend):

    '''
    Computes the average of a variable that contains missing values

    @param var         The name of the variable that is being  averaged.

    @param years       A list of the years that are in this average

    @param hist_dict   A dictionary that holds file references for all years/months. 

    @param ave_info    A dictionary of the type of average that is to be done.
                       Includes:  type, months_to_average, fn, and weights
                       (weights are not used in this function/average)
    
    @param file_dict   A dictionary which holds file pointers to the input files that
                       are needed by this average calculation.

    @param ave_type    The average type key that indicated which type of average will be done.

    @param fillValue   The value that indicates missing values within the data.

    @param timer       The timer class used for time bookkeeping.

    @param depend      Boolean variable to indicate if this average will be computed from previously calculated files.

    @return var_Ave    The averaged results for this variable across the designated time frame.
    '''
    # if variable contains missing values, create a mask accumulator that will count how many masked values not to add & divide
    count = 0
    first = True
    fetch_time = 0

    first_mask = True
    for yr in years:
        i = 0
        for m in ave_info['months_to_average']:
            timer.start("Variable fetch time")
            # Check if doing a winter average and get the correct year to pull
            if ((ave_type == 'djf' and depend == False) or ave_type == 'next_jan'
                    or ave_type == 'next_feb' or ave_type == 'prev_dec'):
                pull_year = climFileIO.which_winter_year(hist_dict, m, yr,years[0])
            else:
                pull_year = yr
            var_val = rover.fetch_slice(hist_dict,pull_year,m,var,file_dict)
            timer.stop("Variable fetch time") 
            var_filled = var_val.filled(fill_value=0) # zero out the masked grid points
            # Get and add mask values to the mask accumulator
            if (first_mask):
                if (MA.any(MA.getmask(var_val))):
                    mask_sum = (MA.getmask(var_val)).astype(int)
                    first_mask = False
            else:
                if (MA.any(MA.getmask(var_val))):
                    mask_sum = mask_sum + (MA.getmask(var_val)).astype(int)
            if (first):
                var_sum = (var_val*ave_info['weights'][i])
                first = False
            else:
                var_sum = (var_val*ave_info['weights'][i]) + var_sum
            i+=1
        count+=1
    # Since the weights are only for 1 year, divide by total number of years
    var_Ave = np.divide(var_sum,count)
    # If any values are 0, then replace the var_Ave value with the fill value
    if (first_mask != True):
        var_Ave[mask_sum>0]=fillValue 

    return var_Ave


def weighted_hor_avg_var_from_yr(var,reg_name,reg_num,mask_var,wgt_var,year,hist_dict,ave_info,file_dict):

    '''
    Computes the weighted hor mean rms diff for a year  

    @param var         The name of the variable that is being  averaged.

    @reg_name          The name of the region to average over.

    @reg_num           The number of the region in the region_mask.

    @mask_var          The name of the netCDF variable that contain the region mask.

    @wgt_var           The name of the netCDF variable that contains the weight information.

    @param year        The year to average over. 

    @param hist_dict   A dictionary that holds file references for all years/months. 

    @param ave_info    A dictionary of the type of average that is to be done.
                       Includes:  type, months_to_average, fn, and weights
                       (weights are not used in this function/average)
    
    @param file_dict   A dictionary which holds file pointers to the input files that
                       are needed by this average calculation.

    @return var_Ave    The averaged results for this variable across the designated time frame.
    '''

    # Get correct data slice from the yearly average file
    var_val = rover.fetch_slice(hist_dict,year,0,var,file_dict)
    # Get the weighted values from the yearly average file
    lev_weights = rover.fetch_slice(hist_dict,year,0,wgt_var,file_dict,time=False).astype(np.float32)
    # Get the region mask
    if (reg_name == 'Glo'):
        temp = rover.fetch_slice(hist_dict,year,0,mask_var,file_dict,time=False)
        lev_region_mask = MA.masked_where(int(reg_num)==temp,temp)
    else:
        temp = rover.fetch_slice(hist_dict,year,0,mask_var,file_dict,time=False)
        lev_region_mask = MA.masked_where(int(reg_num)!=temp,temp)
    # Since weights and region mask are only one level, we need to expand them to all levels
    region_mask = MA.expand_dims(temp, axis=0)
    weights = MA.expand_dims(lev_weights, axis=0)
    if var_val.ndim > 2:
        for lev in range(1,60):
            new_region_mask = MA.expand_dims(temp, axis=0)
            region_mask = np.vstack((region_mask,new_region_mask))
            new_weights = MA.expand_dims(lev_weights, axis=0)
            weights = np.vstack((weights,new_weights))
    else:
        region_mask = np.squeeze(region_mask,axis=0)
        
    # Calculate the weighted average
    # First, we need to reshape the arrays to average along two dims
    if (reg_name == 'Glo'):
        temp_mask = MA.masked_where(region_mask==int(reg_num),var_val)
    else:
        temp_mask = MA.masked_where(region_mask!=int(reg_num),var_val)
    ma_to_average = temp_mask.reshape(temp_mask.shape[0], -1)
    if var_val.ndim > 2:
        weights_flattened = weights.reshape(weights.shape[0],-1)
    else:
        weights_flattened = np.squeeze(weights,axis=0)
    var_Ave = MA.average(ma_to_average,axis=1, weights=weights_flattened)
    
    return var_Ave


def diff_var(var, avg_test_slice, obs_file):

    '''
    Computes the diff for a year  

    @param var            The name of the variable that is being  averaged.

    @param avg_test_slice The average slice to compare against observations.

    @param obs_file       The observation file that contains the results to compare against.

    @return var_Avg_diff  The difference for this variable.
    '''

    # Open obs file and get variable slice 
    obs_slice = climFileIO.open_file_return_var(obs_file,var) 

    # Get the difference between the two variables
    var_Avg_diff = avg_test_slice - obs_slice

    return var_Avg_diff

def weighted_rms_var_from_yr(var,reg_name,reg_num,mask_var,wgt_var,year,hist_dict,ave_info,file_dict,avg_test_slice,obs_file):

    '''
    Computes the weighted rms for a year  

    @param var            The name of the variable that is being  averaged.

    @reg_name             The name of the region to average over.

    @reg_num              The number of the region in the region_mask.

    @mask_var             The name of the netCDF variable that contain the region mask.

    @wgt_var              The name of the netCDF variable that contains the weight information.

    @param year           The year to average over. 
    
    @param hist_dict      A dictionary that holds file references for all years/months. 
        
    @param ave_info       A dictionary of the type of average that is to be done.
                          Includes:  type, months_to_average, fn, and weights
                          (weights are not used in this function/average)
    
    @param file_dict      A dictionary which holds file pointers to the input files that
                          are needed by this average calculation.

    @param avg_test_slice Averaged slice used in this calculation.
 
    @param obs_file       Observation file that contains the values to be used in the caluculation.

    @return nrms          The normalized rms results for this variable.
    '''


    import warnings

    # Get the weighted values from the yearly average file
    lev_weights = rover.fetch_slice(hist_dict,year,0,wgt_var,file_dict,time=False).astype(np.float32)
    # Get the region mask
    if (reg_name == 'Glo'):
        temp = rover.fetch_slice(hist_dict,year,0,mask_var,file_dict,time=False)
        lev_region_mask = MA.masked_where(int(reg_num)==temp,temp)
    else:
        temp = rover.fetch_slice(hist_dict,year,0,mask_var,file_dict,time=False)
        lev_region_mask = MA.masked_where(int(reg_num)!=temp,temp)
    # Since region mask is only one level, we need to expand it to all levels
    region_mask = MA.expand_dims(temp, axis=0)
    weights = MA.expand_dims(lev_weights, axis=0)
    for lev in range(1,60):
        new_region_mask = MA.expand_dims(temp, axis=0)
        region_mask = np.vstack((region_mask,new_region_mask))
        new_weights = MA.expand_dims(lev_weights, axis=0)
        weights = np.vstack((weights,new_weights))

    # Calculate the root mean square
    # First, we need to reshape the arrays to average along two dims
    if (reg_name == 'Glo'):
        temp_mask = MA.masked_where(region_mask==int(reg_num),avg_test_slice)
    else:
        temp_mask = MA.masked_where(region_mask!=int(reg_num),avg_test_slice)

    warnings.filterwarnings("ignore")
    #ma_to_average = MA.array(avg_test_slice, mask=region_mask).reshape(avg_test_slice.shape[0], -1)
    ma_to_average = temp_mask.reshape(temp_mask.shape[0], -1)
    weights_flattened = weights.reshape(weights.shape[0],-1)
    rms_Ave = MA.sqrt(MA.average((ma_to_average*ma_to_average), axis=1, weights=weights_flattened))    
    warnings.filterwarnings("default")

    # Normalize to match NCO rms
    nrms = rms_Ave/(MA.max(rms_Ave) - MA.min(rms_Ave))  

    return nrms

def mean_diff_rms(var,reg_name,reg_num,mask_var,wgt_var,year,hist_dict,ave_info,file_dict,obs_file,reg_obs_file,simplecomm,serial,MPI_TAG):

    '''
    Computes the weighted hor mean rms diff for a year  

    @param var           The name of the variable that is being  averaged.

    @reg_name            The name of the region to average over.

    @reg_num             The number of the region in the region_mask.

    @mask_var            The name of the netCDF variable that contain the region mask.

    @wgt_var             The name of the netCDF variable that contains the weight information.

    @param year          The year to average over. 
    
    @param hist_dict     A dictionary that holds file references for all years/months. 
        
    @param ave_info      A dictionary of the type of average that is to be done.
                         Includes:  type, months_to_average, fn, and weights
                         (weights are not used in this function/average)
    
    @param file_dict     A dictionary which holds file pointers to the input files that
                         are needed by this average calculation.

    @param obs_file      Observational file name

    @param reg_obs_file  Regional observation files

    @simplecomm          Simplecomm object used for mpi communication.

    @serial              Boolean if running in serial or parallel mode.

    @MPI_TAG             Integer tag used to communicate message numbers.

    @return var_Ave      The averaged results for this variable.

    @return var_DIFF     The difference results for this variable.

    @return var_RMS      The normalized rms results for this variable.

    '''

    print('Computing ',ave_info['type'],' for ',var," for ",year, " region ",reg_name)
    var_diff = var+'_DIFF'
    var_rms = var+'_RMS'

    ## Get the masked regional average
    var_Avg = weighted_hor_avg_var_from_yr(var,reg_name,reg_num,mask_var,wgt_var,year[0],hist_dict,ave_info,file_dict)
    ## Send var_Avg results to local root to write
    if (not serial):
        md_message_v = {'name':var,'shape':var_Avg.shape,'dtype':var_Avg.dtype,'average':var_Avg}
        simplecomm.collect(data=md_message_v,tag=MPI_TAG)

    # Get the DIFF values
    var_DIFF = diff_var(var, var_Avg, reg_obs_file)
    # Send var_Diff results to local root to write
    if (not serial):
        md_message = {'name':var_diff,'shape':var_DIFF.shape,'dtype':var_DIFF.dtype,'average':var_DIFF}
        simplecomm.collect(data=md_message,tag=MPI_TAG)


    ## Get the RMS from the obs diff
    var_slice = rover.fetch_slice(hist_dict,year[0],0,var,file_dict)
    temp_diff = diff_var(var, var_slice, obs_file)
    var_RMS = weighted_rms_var_from_yr(var,reg_name,reg_num,mask_var,wgt_var,year[0],hist_dict,ave_info,file_dict,temp_diff,obs_file)
    ## Send var_RMS results to local root to write
    if (not serial):
        md_message = {'name':var_rms,'shape':var_RMS.shape,'dtype':var_RMS.dtype,'average':var_RMS}
        simplecomm.collect(data=md_message,tag=MPI_TAG)

    return var_Avg,var_DIFF,var_RMS 

def time_concat(var,years,hist_dict,ave_info,file_dict,ave_type,simplecomm,all_files_vars,serial):

    '''
    Concats files together in the time dimension.

    @param var             The name of the variable to concat.

    @param years           A list of the years that are in this average

    @param hist_dict       A dictionary that holds file references for all years/months. 

    @param ave_info        A dictionary of the type of average that is to be done.
                           Includes:  type, months_to_average, fn, and weights
                           (weights are not used in this function/average)
    
    @param file_dict       A dictionary which holds file pointers to the input files that
                           are needed by this average calculation.

    @param ave_type        The average type key that indicated which type of average will be done.

    @param simplecomm      The simple comm object used for mpi communication.

    @param all_files_vars  All of the file's variables with ncids attached.

    @serial                Boolean if running in serial mode.

    '''

    print('Concatenating ',ave_info['type'],' for ',var)
    time_index = 0
    CONCAT_TAG = 60
    # Loop over years, months, and variables to cat them all together into one file
    first = True
    for yr in years:
        for m in ave_info['months_to_average']:
            if ('__meta' in var):
                parts = var.split('__')
                var = parts[0]
            # If slave, get slice and pass to master
            if (not simplecomm.is_manager() or serial):
                var_val = rover.fetch_slice(hist_dict,yr,m,var,file_dict)
                if not serial:
                    var_shape = var_val.shape
                    var_dtype = var_val.dtype
                    md_message = {'name':var,'shape':var_shape,'dtype':var_dtype,'average':var_val,'index':time_index}
                    simplecomm.collect(data=md_message,tag=CONCAT_TAG)
            if (simplecomm.is_manager() or serial):
                # If master, recv slice and write to file
                if not serial:
                    r_rank,results = simplecomm.collect(tag=CONCAT_TAG)
                    var_val = results['average']
                    var_n = results['name']
                    ti = results['index']
                else:
                    var_n = var
                    ti = time_index
                climFileIO.write_averages(all_files_vars, var_val, var_n, index=ti) 
            time_index = time_index + 1

def get_metaCharValue(var,years,hist_dict,ave_info,file_dict,timer):

    '''
    Reads a char meta variable from an existing input file to get the value to insert into the new file. 

    @param var         The name of the variable that is being  averaged.

    @param years       A list of the years that are in this average

    @param hist_dict   A dictionary that holds file references for all years/months. 

    @param ave_info    A dictionary of the type of average that is to be done.
                       Includes:  type, months_to_average, fn, and weights
                       (weights are not used in this function/average)
    
    @param file_dict   A dictionary which holds file pointers to the input files that
                       are needed by this average calculation.

    @param timer       The timer class used for time bookkeeping.

    @return var_values Return the char value from an existing file.
    '''

    var_values = rover.fetch_slice(hist_dict,years[0],ave_info['months_to_average'][0],var,file_dict)
    return var_values[0] 
