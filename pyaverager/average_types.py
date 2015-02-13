'''
 Contains a container to hold the directions need for the different types of averaging.
 Required entries for each dictionary average type:
   'months_to_average': A list of months to be looped over and averaged
   'type': Long name of the average
   'fn': The averaged file's suffix.
 Optional:
   'weights':  List the weight values (must have the same length as 'months_to_average').

 To add a new option, create a new key and add the required entries.  New entries should
 follow the coding patterns as the other entries.
____________________________
Created on November 20, 2014

@author: Sheri Mickelson <mickelso@ucar.edu> 
'''

average_types = {
      'ya':{'months_to_average':[0,1,2,3,4,5,6,7,8,9,10,11],'type':'yearly average','fn':'nc',
             'weights':[0.08493150770664215, 0.07671232521533966, 0.08493150770664215, 0.08219178020954132,
                        0.08493150770664215, 0.08219178020954132, 0.08493150770664215, 0.08493150770664215,
                        0.08219178020954132, 0.08493150770664215, 0.08219178020954132, 0.08493150770664215]},
      'tavg':{'months_to_average':[0],'type':'yearly average:tavg','fn':'nc',
             'weights':[0.08493150770664215, 0.07671232521533966, 0.08493150770664215, 0.08219178020954132,
                        0.08493150770664215, 0.08219178020954132, 0.08493150770664215, 0.08493150770664215,
                        0.08219178020954132, 0.08493150770664215, 0.08219178020954132, 0.08493150770664215],
             'depend':['ya'], 'depend_type': 'year'},
      'ann':{'months_to_average':[0,1,2,3,4,5,6,7,8,9,10,11],'type':'annual average','fn':'ANN_climo.nc',
             'weights':[0.08493150770664215, 0.07671232521533966, 0.08493150770664215, 0.08219178020954132,
                        0.08493150770664215, 0.08219178020954132, 0.08493150770664215, 0.08493150770664215,
                        0.08219178020954132, 0.08493150770664215, 0.08219178020954132, 0.08493150770664215],
	     'depend':['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'], 'depend_type': 'month'},
      'djf':{'months_to_average':[11,0,1],'type':'season average, djf','fn':'DJF_climo.nc',
             'weights':[0.3444444537162781, 0.3444444537162781, 0.3111111223697662],
	     'depend':['dec','jan','feb'], 'depend_type': 'month'},
      'mam':{'months_to_average':[2,3,4],'type':'season average, mam','fn':'MAM_climo.nc',
             'weights':[0.3369565308094025, 0.3260869681835175, 0.3369565308094025],
             'depend':['mar','apr','may'], 'depend_type': 'month'},
      'jja':{'months_to_average':[5,6,7],'type':'season average, jja','fn':'JJA_climo.nc',
             'weights':[0.3260869681835175, 0.3369565308094025, 0.3369565308094025],
             'depend':['jun','jul','aug'], 'depend_type': 'month'},
      'son':{'months_to_average':[8,9,10],'type':'season average, son','fn':'SON_climo.nc',
             'weights':[0.32967033, 0.34065934, 0.32967033],
	     'depend':['sep','oct','nov'], 'depend_type': 'month'},
      'jan':{'months_to_average':[0],'type':'monthly average, jan','fn':'01_climo.nc'},
      'next_jan':{'months_to_average':[0],'type':'monthly average, next jan','fn':'next_01_climo.nc'},
      'feb':{'months_to_average':[1],'type':'monthly average, feb','fn':'02_climo.nc'},
      'next_feb':{'months_to_average':[1],'type':'monthly average, next feb','fn':'next_02_climo.nc'},
      'mar':{'months_to_average':[2],'type':'monthly average, mar','fn':'03_climo.nc'},
      'apr':{'months_to_average':[3],'type':'monthly average, apr','fn':'04_climo.nc'},
      'may':{'months_to_average':[4],'type':'monthly average, may','fn':'05_climo.nc'},
      'jun':{'months_to_average':[5],'type':'monthly average, jun','fn':'06_climo.nc'},
      'jul':{'months_to_average':[6],'type':'monthly average, jul','fn':'07_climo.nc'},
      'aug':{'months_to_average':[7],'type':'monthly average, aug','fn':'08_climo.nc'},
      'sep':{'months_to_average':[8],'type':'monthly average, sep','fn':'09_climo.nc'},
      'oct':{'months_to_average':[9],'type':'monthly average, oct','fn':'10_climo.nc'},
      'nov':{'months_to_average':[10],'type':'monthly average, nov','fn':'11_climo.nc'},
      'dec':{'months_to_average':[11],'type':'monthly average, dec','fn':'12_climo.nc'},
      'prev_dec':{'months_to_average':[11],'type':'monthly average, prev dec','fn':'prev_12_climo.nc'},
      'mavg':{'months_to_average':[0,1,2,3,4,5,6,7,8,9,10,11],'type':'monthly average:mavg','fn':'nc',
              'depend':['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'], 'depend_type': 'month'},
      'jfm':{'months_to_average':[0,1,2],'type':'season average, jfm','fn':'jfm_climo.nc'},
      'fm':{'months_to_average': [1,2],'type':'season average, fm','fn':'fm_climo.nc'},
      'amj':{'months_to_average':[3,4,5],'type':'season average, amj','fn':'amj_climo.nc'},
      'jas':{'months_to_average':[6,7,8],'type':'season average, jas','fn':'jas_climo.nc'},
      'ond':{'months_to_average':[9,10,11],'type':'season average, ond','fn':'ond_climo.nc'},
      'on':{'months_to_average': [9,10],'type':'season average, on','fn':'on_climo.nc'}
}

def average_compliance(avg_dict):

    '''
    Examines the average list that user supplies and make sure the format is correct.
    The program will exit if any errors are found.

    @param avg_dict  The list of averages the user would like to compute.        

    '''

    import sys
    import average_types as ave_t

    for ave in avg_dict:
        ave_descr = ave.split(':')
        ave_type = ave_descr[0]

        # Set average name and flag if it's a depend average 
        if 'dep' in ave_type:
            ave_name = ave_type[4:]
            dep = True
        else:
            ave_name = ave_type  
            dep = False
            # If mavg is in the list, make it a depend average
            if ave_name == 'mavg':
                avg_dict[avg_dict.index(ave)] = 'dep_'+ave
            # If tavg is in the list, make it a depend average
            if ave_name == 'tavg':
                avg_dict[avg_dict.index(ave)] = 'dep_'+ave


        # Is average type in list
        if ave_name not in ave_t.average_types:
            print 'ERROR: ', ave, 'is not in the list of know averages. Exiting.'
            sys.exit(1)
  
        # If variable is added avg list as a depend, make sure it can be created this way 
        if dep: 
            if 'depend' not in ave_t.average_types[ave_name]: 
                print 'ERROR: ', ave, 'cannot be created with dependencies.  Please remove \'dep_\' and rerun.  Exiting.'
                sys.exit(2)

        # Check to see if average has correct number of arguments 
        if (ave_name == 'ya'):
            if (len(ave_descr) != 2):
                print 'ERROR: ',ave,' must be formatted avg_type:year.  Exiting.'
                sys.exit(3)
                
        else:
            if (len(ave_descr) != 3):
                print 'ERROR: ',ave,' must be formatted avg_type:start_year:end_year.  Exiting.'
                sys.exit(4)

    print 'Average list complies with standards.'

def sort_depend(avg_dict,i):

    '''
    A recursive function that goes through the user supplied average list and sorts out 
    dependencies into different levels and adds extra averages that are needed by dependency averages.
    Any average that can be computed first will be in the 0 dimension of the avg_dict.  Any depend 
    averages will be in later dimensions of the avg_dict as to be determined by other dependencies.

    @param avg_dict  The list of averages the user would like to compute.        

    @return avg_dict The sorted list averages supplied by the user.  The list is sorted by which averages
                     should be computed first, then second, and so on.

    '''

    import sys
    import average_types as ave_t

    dependencies = [s for s in avg_dict[i] if 'dep' in s]
    #print avg_dict[i]
    #print i
    if (len(dependencies) > 0):
        avg_dict[i+1] = []
        temp_missing = []
        type_list = []
        short_type_list = []
        for ave in avg_dict[i]:
            ave_descr = ave.split(':')
            short_type_list.append(ave_descr[0])
            type_list.append(ave) 
            if ('djf' in ave_descr[0]):
                avg_dict[i].append('prev_dec'+ave[len(ave_descr[0]):])
                avg_dict[i].append('next_jan'+ave[len(ave_descr[0]):])
                avg_dict[i].append('next_feb'+ave[len(ave_descr[0]):])
        for ave in dependencies:
            ave_descr = ave.split(':')
            ave_type = ave_descr[0][4:]
            avg_dict[i].remove(ave)
            avg_dict[i+1].append(ave_descr[0][4:]+ave[len(ave_descr[0]):]+":__d")
            #print 'dependencies for ',ave_type,': ',ave_t.average_types[ave_type]['depend']
            for depend in ave_t.average_types[ave_type]['depend']:
                new_depend = [s for s in ave_t.average_types[ave_type]['depend'] if 'dep' in s]
                if (len(new_depend) > 0):
                    avg_dict[i+1].remove(ave_descr[0][4:]+ave[len(ave_descr[0]):]+":__d")
                    avg_dict[i+1].append(ave)
                if (ave_t.average_types[ave_type]['depend_type'] == 'year'):
                    years = range(int(ave_descr[1]),int(ave_descr[2])+1)
                    for yr in years:
                        depend_plus_date = depend+":"+str(yr)
                        if (depend_plus_date not in type_list):
                            temp_missing.append(depend_plus_date)
                else:
                    depend_plus_date = depend+ave[len(ave_descr[0]):]
                    if (depend_plus_date not in type_list):
                        if (depend not in short_type_list):
                            temp_missing.append(depend_plus_date)
                        else: # average is in the list, but different date range, flag as an error for now
                            print "ERROR: Need to add ",depend_plus_date," to average list for ",ave,", but another",depend, "has already been added with a different date range.  Only one may exist. Exiting."
                            sys.exit(5)
        missing = set(temp_missing)
        avg_dict[i] = avg_dict[i] + list(missing)
        return sort_depend(avg_dict,i+1)
    else:
        return avg_dict

