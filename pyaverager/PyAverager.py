def run_pyAverager(spec):

    '''
    A callable routine users call to start computing averages.  Returns an
    instance of the PyAverager when all averages have been computed.

    @param spec          An instance of the Specification class which holds the user settings
                         that define which averages to compute, directories, file prefixes, etc

    @return PyAverager   An instance of the PyAverager class.
    '''    
    
    return PyAverager(spec)


class PyAverager(object):

    def __init__(self,spec):

        '''
        Calls the compute_averages function to setup and compute the needed averages.

        @param spec          An instance of the Specification class which holds the user settings
                             that define which averages to compute, directories, file prefixes, etc    
        '''
        self.compute_averages(spec)


    def compute_averages(self,spec):

        '''
        Sets up the run information and computes the averages.

        @param spec          An instance of the Specification class which holds the user settings
                             that define which averages to compute, directories, file prefixes, etc
        '''
        import datetime
        import os,sys
        import rover
        import climAverager
        import climFileIO
        import average_types as ave_t
        import regionOpts
        import string
        from timekeeper import TimeKeeper
        from messenger import create_messenger
        from mpi4py import MPI
#==============================================================================
#
# Initialize 
#
#==============================================================================
        # Initialize the timekeeper class and start 'total' timer
        timer = TimeKeeper()
        timer.start("Total Time")
        # Initialize some timers that are not used by all tasks
        timer.reset("Send Average Time")
        timer.reset("Variable fetch time")
        timer.reset("Recv Average Time")
        timer.reset("Write Netcdf Averages")
        timer.reset("Variable fetch time")
        timer.reset("Time to compute Average")

        # Initialize the messenger class
        messenger = create_messenger(serial=spec.serial)

        # Check average list to make sure it complies with the standards
        ave_t.average_compliance(spec.avg_list)

        # Sort through the average list and figure out dependencies and do
        # averages in steps if need be.
        avg_dict = {0:spec.avg_list}
        avg_dict = ave_t.sort_depend(avg_dict,0)
        print avg_dict
        for i in range(0,len(avg_dict)):
         
            # Initialize some containers 
            var_list = []
            full_hist_dict = {}
            hist_dict = {}
#==============================================================================
#
# Set the hist_dict up with file references for all years/months.
# Create a list of all variables and meta variables within the file
# and set the final variable list passed on user preferences. 
#
#==============================================================================

            ## Set var_list and file info dictionary
            timer.start("Define history dictionary")
            if (spec.hist_type == 'series'):
                full_hist_dict,full_var_list,meta_list,key = rover.set_slices_and_vars_time_series(spec.in_directory, spec.file_pattern, spec.prefix, spec.year0, spec.year1,
                                                    spec.split)
            else:
                full_hist_dict,full_var_list,meta_list,key = rover.set_slices_and_vars_time_slice(spec.in_directory, spec.file_pattern, spec.prefix, spec.year0, spec.year1)
            timer.stop("Define history dictionary")

            # Set variable list.  If there was a variable list passed to the averager, use this list.  Other wise,
            # use all variables within the file.

            if (len(spec.varlist)>0):
                var_list = spec.varlist
            else:
                var_list = full_var_list

#==============================================================================
#
# Workload Distribution
#
#==============================================================================

            # Each intercommunicator recieves a list of averages it's responsible for
            # Each mpi task within that intercommunicator gets a portion of the variable list 

            num_of_avg = len(avg_dict[i])
            min_procs_per_ave = 4

            # Override user selection if they picked less than 2 or
            # the variable list is less than the min procs per sub-communicator
            if (min_procs_per_ave < 2 or len(var_list) < (min_procs_per_ave-1)):
                min_procs_per_ave = 2

            # set comms
            if spec.serial == True :
                comm = 0
            else :
                comm = MPI.COMM_WORLD

            size = messenger.get_size(comm)
            rank = messenger.get_rank(comm)

            # split mpi comm world
            intercomm,color = messenger.split_comm(rank, num_of_avg, min_procs_per_ave, comm)
            lsize = messenger.get_size(intercomm)
            lrank = messenger.get_rank(intercomm)

            g_master = messenger.is_master(comm)
            l_master = messenger.is_master(intercomm)

            # Partion the average task list amoung the inter/split communicators
            laverages = messenger.partition_across_comms(color,avg_dict[i])

            # Partition the variable list between the tasks of each communicator
            if (lsize > 1):
                if not l_master:
                    lvar_list = messenger.partition(var_list, comm=intercomm, size=lsize-1, rank=lrank-1)
                else:
                    lvar_list = var_list
            else:
                lvar_list = var_list

#            print(rank,'averages :',laverages)
#            print(rank,'vars :',lvar_list)

#==============================================================================
#
# Create the output directory if it doesn't exist
#
#==============================================================================

            if spec.serial or g_master:
                if not os.path.exists(spec.out_directory):
                    os.makedirs(spec.out_directory)

#==============================================================================
#
# Main Averaging Loop
#
#==============================================================================
            # Files are only split for the first loop.  When the depend averages start, they will operate on files
            # that are already stiched together.
            if (i != 0):
                spec.split_name = 'null'
                spec.split = False
                spec.split_files = 'null'
 
            for ave in laverages:
                for split_name in spec.split_files.split(","): 
                    # Split apart the average info to get type of average and year(s) 
                    ave_descr = ave.split(':')

                    # If the average depends on other averages that have to be computed, create a new temporary dictionary
                    if '__d' in ave_descr:
                        yr0 = ave_descr[1]
                        if (len(ave_descr) > 2):
                           yr1 = ave_descr[2]
                        else:
                           yr1 = ave_descr[1]
                        hist_dict = rover.set_slices_and_vars_depend(spec.out_directory, spec.file_pattern, spec.prefix, yr0, yr1,
                                                                            ave_t.average_types[ave_descr[0]],ave_descr[0])
                    else:
                        hist_dict = dict(full_hist_dict)   
                    
                    # Create and define the average file 
                    timer.start("Create/Define Netcdf File")
                    if ('mavg' in ave_descr or 'tavg' in ave_descr):
                        date1 = string.zfill(ave_descr[1],4)
                        date2 = string.zfill(ave_descr[2],4)
                        ave_date = date1+'-'+date2
                    else:
                        ave_date = string.zfill(ave_descr[1],4)
                    outfile_name = climFileIO.get_out_fn(ave_descr[0],spec.prefix,ave_date,ave_t.average_types[ave_descr[0]]['fn'])
                    all_files_vars,new_file = climFileIO.define_ave_file(l_master,spec.serial,var_list,lvar_list,meta_list,hist_dict,
                                                    	                 spec.hist_type,ave_descr,spec.prefix,outfile_name,
                                                                         intercomm,spec.split,split_name,spec.out_directory,messenger,
									 spec.ncformat,ave_t.average_types[ave_descr[0]]['months_to_average'][0],key) 
                    timer.stop("Create/Define Netcdf File")
                   
                    # Start loops to compute averages
                    # create a list of years that are needed for this average
                    years = []
                    if '__d' in ave_descr:
                        if (ave_t.average_types[ave_descr[0]]['depend_type'] == 'month'):
                            years.append(int(ave_descr[1]))
                        else:
                            years = list(range(int(ave_descr[1]),int(ave_descr[2])+1))
                        depend = True
                    else: 
                        if (len(ave_descr) == 2):
                            years.append(int(ave_descr[1]))
                        else:
                            years = list(range(int(ave_descr[1]),int(ave_descr[2])+1))
                        depend = False

                    # Open all of the files that this rank will need for this average (for time slice files)
                    if ((spec.hist_type == 'slice' or '__d' in ave_descr)  and (spec.serial or not l_master) and len(lvar_list) > 0):
                        file_dict,open_list = climFileIO.open_all_files(hist_dict,ave_t.average_types[ave_descr[0]]['months_to_average'],
		                                                years,lvar_list[0],'null',ave_descr[0],depend)

                    # If concat of file instead of average, piece file together here.  If not, enter averaging loop
                    if ('mavg' in ave_descr):
                        # Since this is a serial process, only have the local root do the work
                        if l_master:
                            # Open files
                            file_dict,open_list = climFileIO.open_all_files(hist_dict,ave_t.average_types[ave_descr[0]]['months_to_average'],
                                                                years,lvar_list[0],'null',ave_descr[0],depend)
                            # Concat the slices together
                            climAverager.time_concat(lvar_list,years,hist_dict,ave_t.average_types[ave_descr[0]],
						     file_dict,ave_descr[0],all_files_vars)
                        # Close the files that were opened for reading
                        climFileIO.close_all_files(open_list)
                    else:
                        # Loop through variables and compute the averages
                        for orig_var in lvar_list:
                            # Some variable names were suffixed with a meta label indicaticating that the variable exists in all files,
                            # but there isn't a didicated ts file to open.  Pick the first variable off the list and get values from there
                            if ('__meta' in orig_var):
                                var = key 
                            else:
                                var = orig_var
                            # Open all of the files that this rank will need for this average (for time series files)
                            if ((spec.hist_type == 'series' and '__d' not in ave_descr) and (spec.serial or not l_master)):
                                file_dict,open_list = climFileIO.open_all_files(hist_dict,ave_t.average_types[ave_descr[0]]['months_to_average'],
		             	                                                years,var,split_name,ave_descr[0],depend)
                            # We now have open files to pull values from.  Now reset var name
                            if ('__meta' in orig_var):
                                parts = orig_var.split('__')
                                var = parts[0]
                            if spec.serial or not l_master:
                                if ('__metaChar' in orig_var):
                                    var_avg_results =  climAverager.get_metaCharValue(var,years,hist_dict,ave_t.average_types[ave_descr[0]],
								file_dict,timer) 
                                else: 
                                    # Average
                                    if (spec.weighted == True and 'weights' in ave_t.average_types[ave_descr[0]]):
                                        var_avg_results =  climAverager.weighted_avg_var(var,years,hist_dict,
	                                      ave_t.average_types[ave_descr[0]],file_dict,ave_descr[0],timer,depend)
                                    else:
                                        var_avg_results =  climAverager.avg_var(var,years,hist_dict,
	                                    ave_t.average_types[ave_descr[0]],file_dict,ave_descr[0],timer,depend)
      
                                # Close all open files (for time series files)
                                if ((spec.hist_type == 'series' and '__d' not in ave_descr) and (spec.serial or not l_master)):
                                    climFileIO.close_all_files(open_list)

                                # Pass the average results to master rank for writing
                                var_shape = var_avg_results.shape
                                var_dtype = var_avg_results.dtype
                                md_message = {'name':var,'from_rank':lrank,'shape':var_shape,'dtype':var_dtype}
                                if not spec.serial:
                                    timer.start("Send Average Time")
                                    messenger.Send_npArray(md_message, var_avg_results, 0, intercomm)
                                    timer.stop("Send Average Time")
        
                            if spec.serial or l_master:
                                if not spec.serial:
                                    timer.start("Recv Average Time")
                                    var,var_avg_results = messenger.Recv_npArray(intercomm)
                                    timer.start("Recv Average Time") 

                                timer.start("Write Netcdf Averages")
                                climFileIO.write_averages(all_files_vars, var_avg_results, var)
                                timer.stop("Write Netcdf Averages")

                        # Close all open files (for time slice files)
                        if ((spec.hist_type == 'slice' or '__d' in ave_descr)and (spec.serial or not l_master) and len(lvar_list) > 0):
                            climFileIO.close_all_files(open_list)  
       
                        # Sync the local communicator before closing the averaged netcdf file and moving to the next average          
                        messenger.sync(intercomm)
 
                    # Close the newly created average file
                    if spec.serial or l_master:
                        new_file.close()

                # If needed, stitch spatially split files together.
                if spec.serial or l_master:
                    if (len(spec.split_files.split(",")) > 1):
                        fn1 = spec.out_directory+'nh_'+outfile_name
                        fn2 = spec.out_directory+'sh_'+outfile_name
                        out_fn = spec.out_directory+outfile_name
                        dim_info = spec.split_orig_size.split(",")
                        dim1 = dim_info[0].split("=")
                        dim2 = dim_info[1].split("=")
                        regionOpts.combine_regions(fn1, fn2,  out_fn, dim1[0], int(dim1[1]), dim2[0], int(dim2[1]), "nj") 
            
            if not spec.serial:
                # Free the inter-communicators
                intercomm.Free()
                # Sync all mpi tasks / All averages should have been computed at this point 
                messenger.sync(comm)

#==============================================================================
#
# Collect and print timing information
#
#==============================================================================

        timer.stop("Total Time")
        my_times = messenger.max(timer.get_all_times())

        if g_master:
            print("==============================================")
            print my_times
            print("==============================================") 
