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
    var_Ave[np.isnan(var_Ave)]=fillValue

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


def time_concat(full_var_list,years,hist_dict,ave_info,file_dict,ave_type,all_files_vars):

    '''
    Concats files together in the time dimension.

    @param full_var_list   The names of the variables that are being averaged.

    @param years           A list of the years that are in this average

    @param hist_dict       A dictionary that holds file references for all years/months. 

    @param ave_info        A dictionary of the type of average that is to be done.
                           Includes:  type, months_to_average, fn, and weights
                           (weights are not used in this function/average)
    
    @param file_dict       A dictionary which holds file pointers to the input files that
                           are needed by this average calculation.

    @param ave_type        The average type key that indicated which type of average will be done.

    @param all_files_vars  All of the file's variables with ncids attached.

    '''

    print('Concatenating ',ave_info['type'],' for all variables for ',years)
    time_index = 0
    # Loop over years, months, and variables to cat them all together into one file
    for yr in years:
        for m in ave_info['months_to_average']:
            for var in full_var_list:
                if ('__meta' in var):
                    parts = var.split('__')
                    var = parts[0]
                # Read from input file
                var_val = rover.fetch_slice(hist_dict,yr,m,var,file_dict)
                # Write to concat to output file
                if var_val.shape:
                    all_files_vars[var][time_index] = var_val[:]
                else:
                    all_files_vars[var][time_index] = var_val
            time_index+=1

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
