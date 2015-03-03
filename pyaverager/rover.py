import glob,sys,os
import Nio
import time

def set_slices_and_vars_time_series(directory, file_pattern, prefix, start_yr, end_yr, split):

    '''
    Create a  dictionary lookup based on time series files
    Also creates a list of variables to average and a list of meta vars

    @param directory      The directory where the input data is located.

    @param file_pattern   The file pattern to glob the input directory on.

    @param prefix         The prefix to glob the input directory on.

    @param start_yr       The first year that will be needed by the average(s).

    @param end_yr         The last year that will be needed by the average(s).

    @param split          Boolean, if input files are spit spatially.        

    @return hist_dict     A dictionary that lists all input file references for each
                          year/month needed by all averages.

    @return series_list   A list of all the variables within the input files that can
                          be averaged.

    @return meta_list     A list of the metadata that will not be averaged, but should be
                          included in the averaged/output file.
    
    @return key           A variable to use that has a specific file attached to that name.
                          Used as the file to retreive meta data from.
    '''  


    # We want to search for the previous year and the year after the last 
    # in case the averaging needs them
    if start_yr > 1:
        start_yr = start_yr - 1
    end_yr = end_yr + 1

    # Glob the directory and get a list of all matching names
    glob_string = directory+ "/" + prefix + "*.nc"
    file_list = glob.glob(glob_string)

    # Foreach of the files, get date strings and get var list
    dates = []
    var_list = []
    for f in file_list:
        name_parts = f.split(".")
        np_len = len(name_parts)
        dates.append(name_parts[np_len-2])
        if split:
            var_list.append(name_parts[np_len-3][:-3])
        else:  
            var_list.append(name_parts[np_len-3])
    # remove duplicates by converting to a set
    date_list = set(dates)
    series_list = set(var_list)
    key = var_list[0]

    # Go through date_list and create a dictionary of the date breakdown
    date_lookup = {}
    for date in date_list:
        date_breakdown = {}
        date_split = date.split("-")
        date_breakdown["year1"] = int(date_split[0][0:4])
        date_breakdown["month1"] = int(date_split[0][4:6])
        date_breakdown["year2"] = int(date_split[1][0:4])
        date_breakdown["month2"] = int(date_split[1][4:6]) 
        date_lookup[date] = date_breakdown

    # Go through each year to average and make sure it exists within a found date range
    years = list(range(start_yr,end_yr+1))
    year_list = {}
    for yr in years:
        found = 0
        for stamp,date in date_lookup.items():
            if (yr >= date["year1"] and yr <= date["year2"]):
                if (found == 0):
                    found = 1
                    previousMonth = date["month2"] 
                    year_list[yr] = [stamp]
                else:
                    if (yr == date["year1"]):
                        if (previousMonth == (date["month1"]-1)):
                            year_list[yr].append(stamp)
                        else:
                            print("ERROR: Split year -- doesn't look contiguous. Exiting.") 
                            sys.exit(22)
                    else:
                        print("ERROR: Found more than 1 file that contains year ", yr, ".  Exiting.")
                        sys.exit(23)
            else:
                if (found == 0):    
                    year_list[yr] = []
    # Are file dates contiguous?
    first = 1
    previous_year = 0
    previous_month = 0
    for stamp,date in date_lookup.items():
        if first == 1:
            previous_year = date["year2"]
            previous_month = date["month2"]
            first = 0 
        else:
            if ((previous_year == (date["year1"]-1) and (previous_month == 12 and date["month1"] == 1)) or 
		((previous_year == date["year1"]) and (previous_month == (date["month1"] - 1)))):
                previous_year = date["year2"]
                previous_month = date["month2"]
            #else:
            #    print("ERROR: There's a break in the sequence -- date stamps do not appear contiguous. Exiting.")
            #    sys.exit(22)
    # Create date/slice lookup table
    hist_dict = {}
    for yr in years:
        year_dict = {}
        if (len(year_list[yr]) < 1):
            if (yr != start_yr and yr != end_yr):
                print("ERROR: Did not find file for year",yr,".  Exiting.")
                sys.exit(20)
        for stamp in year_list[yr]:
            found = 0
            start_month = 1
            end_month = 12
            yr1 = date_lookup[stamp]["year1"]
            yr2 = date_lookup[stamp]["year2"]
            m1 = date_lookup[stamp]["month1"]
            m2 = date_lookup[stamp]["month2"]
            file_prefix = directory+ "/" + prefix
            
            # Find the start and end months on the files for indexing
            if (yr > yr1 and yr < yr2):
                found = 1
            elif(yr == yr1):
                if (m1 == 1):
                    found = 1
                else:
                    found = 1
                    start_month = m1
            elif(yr == yr2):
                if (m2 == 12):
                    found = 1
                else:
                    found = 1
                    end_month = m2


            # Set index for that month
            if (found == 1):
                months = list(range(start_month,end_month+1))     
                for m in months:
                    if (m1 == 1):
                        startIndex = (((yr - yr1)*12)+m)-1
                    else:
                        if(m < m1):
                            startIndex = ((((yr - yr1)-1)*12)+(12-m1+1)+m)-1
                        else:
                            startIndex = (((yr-yr1)*12)+(m-m1)+1)-1
                    # set the information for this month slice
                    year_dict[m-1] = {'fn':file_prefix, 'index':startIndex, 'date_stamp':stamp}
        # Add the year's info to the master dictionary
        hist_dict[yr] = year_dict

    # Now we just need to create a meta_list.  
    # Open first file from the file names we globbed earlier,
    # create a list of all variables in the file, 
    # take out the series var that is used in the file name, 
    # and list should be complete then.
    f = Nio.open_file(file_list[1],"r")
    temp_meta_list = list(f.variables.keys())
    name_parts = file_list[1].split(".")
    np_len = len(name_parts)
    if split:
        series_var = name_parts[np_len-3][:-3]
        #print(series_var)
    else:
        series_var = name_parts[np_len-3]
    temp_meta_list.remove(series_var)

    # find the unlimited dimesnion
    dimNames = list(f.dimensions.keys())
    for dim in dimNames:
        if (f.unlimited(dim)):
            unlimited = dim

    # Construct of meta var list
    meta_list = []  
    for var in temp_meta_list:
        if_series,if_variant,if_char = check_if_series_var(f,var,unlimited)
        if (if_series == False and if_variant == False):
            meta_list.append(var)
        else:
            if if_char:
                series_list.add(var+'__metaChar')
            else:
                series_list.add(var+'__meta')
    return hist_dict,list(series_list),list(meta_list),key


def set_slices_and_vars_time_slice(directory, file_pattern, prefix, start_yr, end_yr):

    '''
    Create the dictionary to look up slices based on history time slice files
    Also creates a list of vars to average over and a list of meta vars

    @param directory      The directory where the input data is located.

    @param file_pattern   The file pattern to glob the input directory on.

    @param prefix         The prefix to glob the input directory on.

    @param start_yr       The first year that will be needed by the average(s).

    @param end_yr         The last year that will be needed by the average(s).

    @return hist_dict     A dictionary that lists all input file references for each
                          year/month needed by all averages.

    @return series_list   A list of all the variables within the input files that can
                          be averaged.

    @return meta_list     A list of the metadata that will not be averaged, but should be
                          included in the averaged/output file.

    @return key           A variable to use that has a specific file attached to that name.
                          Used more in when using time series files.
    '''
    # We want to extend the start and stop years by one year on both sides in case
    # extra months are needed  
    if start_yr > 1:
        yr1 = start_yr - 1
    else:
        yr1 = start_yr
    yr2 = end_yr + 1

    hist_dict = {}
    years = list(range(yr1,yr2+1))
    months = list(range(1,13)) 
    for yr in years:
        year_dict = {}
        for m in months:
            # Check to see if the file exists before adding info to dictionary
            startIndex = 0 # Slice index will always be 1 in history time slice files
            file_prefix = directory+"/"+prefix
            yrS = str(yr)
            mS = str(m)
            stamp = yrS.zfill(4)+"-"+mS.zfill(2)
            filename = file_prefix+"."+stamp+".nc"
            if (os.path.isfile(filename)):
                # If exists, add it    
                year_dict[m-1] = {'fn':file_prefix, 'index':startIndex, 'date_stamp':stamp}
            else:
                if (yr > yr1 and yr < yr2):
                    print("ERROR: Could not find file: ",filename,"  Exiting.")
                    sys.exit(20)
        hist_dict[yr] = year_dict 

  
    # Grab variable list from a file.
    yrS = str(start_yr).zfill(4)
    test_file = directory+"/"+prefix+"."+yrS+"-02.nc" 
    f = Nio.open_file(test_file,"r")
    var_list = list(f.variables.keys())

    # Get the unlimited dimension and loop through all variables to check and see if it's a time series var
    dimNames = list(f.dimensions.keys())
    for dim in dimNames:
        if (f.unlimited(dim)):
            unlimited = dim

    series_list = []
    meta_list = []
    for var in var_list:
        if_series,if_variant,if_char = check_if_series_var(f,var,unlimited)
        if (if_series == False and if_variant == False):
            meta_list.append(var)
        elif (if_series == True and if_variant == True):
           series_list.append(var)
    
    f.close()
    key = series_list[0]

    return hist_dict,series_list,meta_list,key


def set_slices_and_vars_depend(directory, file_pattern, prefix, start_yr, end_yr, ave_type, ave):

    '''
    Create the dictionary to look up slices based on history time slice files
    Also creates a list of vars to average over and a list of meta vars

    @param directory      The directory where the input data is located.

    @param file_pattern   The file pattern to glob the input directory on.

    @param prefix         The prefix to glob the input directory on.

    @param start_yr       The first year that will be needed by the average(s).

    @param end_yr         The last year that will be needed by the average(s).

    @param ave_type       The average type key that indicated which type of average will be done.

    @param ave            The average type name string.

    @return hist_dict     A dictionary that lists all input file references for each
                          year/month needed by all averages.

    '''

    import average_types as ave_t
    import string

    hist_dict = {}
    if (ave_type['depend_type'] == 'month'):
        # If depend_type relies on monthly averaged files, define a hist dictionary with only 1 year
        # with non-null values for any average it will use for this new average.
        months_in_year = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        m = 0 # month index
        year_dict = {}
        yr = int(start_yr)
        for mon in months_in_year:
            if (mon in ave_type['depend']):
                if (ave == 'djf'):
                    if (mon == 'jan' or mon == 'feb'): 
                        glob_string = directory + "/" + prefix + '*next_' + ave_t.average_types[mon]['fn']
                    else:
                        glob_string = directory + "/" + prefix + '*prev_' + ave_t.average_types[mon]['fn']
                else:
                    glob_string = directory + "/" + prefix + '*' + ave_t.average_types[mon]['fn']
                file_list = glob.glob(glob_string)
                year_dict[m] = {'fn': file_list[0], 'index':0, 'date_stamp':mon}
            else:
                year_dict[m] = {'fn': 'null', 'index':0, 'date_stamp':mon}            
            m = m + 1 #increase the month index
        hist_dict[yr] = year_dict
    else:
        # depend_type instead relies on yearly averaged files.  The dictionary will contain
        # keys for all years needed in the average, with each month set to the same yearly
        # averaged file.
        years = list(range(int(start_yr),int(end_yr)+1)) 
        for yr in years:
            year_dict = {}    
            yr_fmt = string.zfill(yr,4)
            glob_string = directory + "/" + prefix + "." + yr_fmt + ".*"
            file_list = glob.glob(glob_string)
            for m in range(0,12):
                year_dict[m] = {'fn': file_list[0], 'index':0, 'date_stamp':yr_fmt}
            hist_dict[yr] = year_dict
    return hist_dict

 
def check_if_series_var(f, vn, unlimited):

    '''
     Check to see if the variable if a time series variable or meta variable.
     This is only called by the slice routine.  By nature, a time series file
     should already have this sorted out based on it's file name.    

    @param f            The pointer to an input file.

    @param vn           The name of the variable to determine if it's a series variable.

    @param unlimited    The name of the unlimited dimension within the input NetCDF file.

    @return if_series   Boolean, if the variable has characteristics of a series variable.
 
    @return if_variant  Boolean, if the variable contains the time dimension.
    '''

    if_series = True
    if_char = False
    var = f.variables[vn]

    if (vn == unlimited):
        if_series = False
    # if number of dims is less than or equal to one, not a series var
    elif (var.rank<2):
        if_series = False
    # if it doesn't contain the unlimited dimension (time), not a series var
    elif (unlimited not in var.dimensions):
        if_series = False  
    elif (var.typecode() == 'S1'):
        if_series = False
        if_char = True

    if (unlimited in var.dimensions):
        if_variant = True
    else:
        if_variant = False

#    if (var.typecode() == 'S1'):
#        if_series = False
#        if_variant = False
    return if_series,if_variant,if_char 

def fetch_slice(hist_dict, yr, month, var, file_dict):

    '''
    Based on indexing found within the file_dictionary, return the correct data slice

    @param hist_dict      A dictionary of file references for all years/months that will be averaged.

    @param yr             The year to retrv.

    @param month          The month to retrv.

    @param var            The variable to retrv.

    @param file_dict            Dictionary containing file pointers to the open NetCDF files.

    @return var_val       The time slice that was requested in numPy array format.
    '''

    var_hndl = file_dict[yr][month]['fp'].variables[var]
    var_val = var_hndl[hist_dict[yr][month]['index']]

    return var_val

