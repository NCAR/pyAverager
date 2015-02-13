

#########################################################################################################
#
# Create specifier factory function
#
#########################################################################################################

def create_specifier(**kwargs):

  '''
  Factory function for Specifier class objects

  @param kwargs Optional agruments to be passed to the newly created Specifier constructor.

  @return An instantiation of the Specifier class

  '''

  return pyAveragerSpecifier(**kwargs)


#########################################################################################################
#
# Specifier Base Class
#
#########################################################################################################

class Specifier(object):
    '''
    This is the base class for the pyAverager input specification.
    '''

    def __init__(self):
        '''
        Constructor
        '''

        ## String specifier type
        self.specifier_type = 'undetermined'



#########################################################################################################
#
# Input Specification Class for the pyAverager
#
#########################################################################################################

class pyAveragerSpecifier(Specifier):
  '''
  This class is a container for the input data required by the pyAverager

  '''

  def __init__(self,in_directory,
	       out_directory,
	       prefix,
    	       file_pattern,
	       hist_type='slice',
	       avg_list=[],
  	       weighted=False,
               split=False,
               split_files='null',
	       split_orig_size='null',
	       ncformat='netcdf4c',
	       varlist=[],
	       serial=False):
    '''
    Initializes the internal data with optional arguments

    @param in_directory     Where the input directory resides (needs full path).

    @param out_directory    Where the output will be produced (needs full path).

    @param prefix           String specifying the full file name before the date string.

    @param file_pattern     File pattern used put the prefix, date, and suffix together for input files.

    @param hist_type	    Type of file ('slice' or 'series').  Default is 'slice'.

    @param avg_list	    List of averages that need to be computed.  Elements should contain aveType:year0:year1.
	                    year2 is only required for multi year averaging.

    @param weighted         Boolean variable to selected if weights will be applied to the averaging.  
			    True = weights will be applied.  Default is False.

    @param split            Boolean variable.  True = the file is split spatially and the final average needs to be pieced together.
			    (ie. CICE times series files) Default is False. 

    @param split_files	    The strings indicating the naming difference between split files.  Expects a string with elements separated by a comma.
         	            Defualt is 'null'.  

    @param split_orig_size  A string listing the lat and lon values of the origianl grid size.  Needed in case some of the grid has been deleted.
		            (example: 'lon=288,lat=192').  Default is 'null'.

    @param ncformat	    Format to output the averaged file(s) in.  Default is 'netcdf4c'.  Other options: 'netcdf','netcdf4','netcdf4c'

    @param varlist	    Optional variables list, if not averaging all variables
 
    @param serial	    Boolean to run in serial mode.  True=serial (without MPI) False=run in parallel(with MPI) False requires mpi4py to be installed.
                            Default is False.
 
    '''

    # Where the input is located
    self.in_directory = in_directory

    # Where the output should be produced
    self.out_directory = out_directory

    # Full file name up to the date string
    self.prefix = prefix

    # File pattern used to piece together a full file name
    self.file_pattern = file_pattern

    # Type of file
    self.hist_type = hist_type

    # List of averages to compute
    self.avg_list = avg_list

    # Should weights be applied?
    self.weighted = weighted

    # Are files split spatially?
    self.split = split

    # Split file name indicators
    self.split_files = split_files

    # The original grid size of the split files
    self.split_orig_size = split_orig_size

    # The netcdf output format 
    self.ncformat = ncformat

    # Varlist to average (if not all variables)
    self.varlist = varlist

    # Run in serial mode?  If True, will be ran without MPI
    self.serial = serial

    # Get first and last years used in the averaging by parsing the avg_list
    dates = []
    for avg in avg_list:
      avg_descr = avg.split(':')
      for yr in avg_descr[1:]:
        dates.append(yr)
    self.year0 = int(min(dates))
    self.year1 = int(max(dates)) 
      
