'''
This is the Parallel Utilities class to provide basic load-balancing and
decomposition routines for the PyReshaper.  This encapsulates all of the
mpi4py calls as needed.  It also has the ability to detect if the mpi4py
module is present.  If not, it throws an exception.

_______________________
Created on Apr 30, 2014

@author: Kevin Paul <kpaul@ucar.edu>
@modified by: Sheri Mickelson <mickelso@ucar.edu>
'''

import sys
import math
import numpy as np
from mpi4py import MPI

#==============================================================================
# create_messenger factory function
#==============================================================================
def create_messenger(serial=False):
    '''
    This is the factory function the creates the necessary decomposition
    object for parallel (or serial) operation.  The type must be specified
    by the user with the 'serial' argument, as there is not portable way
    of determining if the run should be assumed to be serial or parallel
    from the environment.

    @param serial  True or False, indicating whether the serial or parallel
                   decomposition utility object should be constructed and
                   returned.  DEFAULT: False (parallel operation)

    @return  A decomposition utility object.
    '''
    # Check type
    if (type(serial) is not bool):
        err_msg = "The serial argument must be a bool."
        raise TypeError(err_msg)

    # Construct and return the desired decomp utility
    if (serial):
        return Messenger()
    else:
        return MPIMessenger()


#==============================================================================
# Messenger Base Class
#==============================================================================
class Messenger(object):
    '''
    This is the base class for decomposition/parallel utilities.  This defines
    serial operation, and has no dependencies.  These methods are reimplemented
    in the derived class for parallel decomposition.
    '''

    def __init__(self):
        '''
        Constructor
        '''

        ## The type of decomp utility constructed
        self.messenger_type = 'serial'

        ## Whether this is the master process/rank
        self._is_master = True

        ## The rank of the processor
        self._mpi_rank = 0

        ## Size of the MPI communicator
        self._mpi_size = 1

        ## Indicates verbosity level
        self.verbosity = 1

    def split_comm(self, rank, list_size, new_comm_size=-1, comm=0):
        '''
        Splits the given communicator into subcommunicators.  Does
        nothing in serial.

        @param rank 	      The rank of the mpitask that is calling this function.
 
        @param list_size      The total number of tasks that need to be performed.

        @param new_comm_size  The minimum number of mpitasks per subcommunicator. Default is -1 for serial mode.

        @param comm           The parent comminucator to split from.  Default is 0 for serial mode.

        @return intercomm     The new subcommincator that this rank is part of.

        @return color	      Which group this rank is part of. 
        '''
        color = 0 
        intercomm = 0

        return intercomm,color

    def partition(self, global_items, comm=0, size=-1, rank=-1):
        '''
        Given a container of items, this algorithm selects a subset of
        items to be used by the local process.  If the 'global_items' object
        is a dictionary, then the values of the dictionary are treated as
        weights for the partitioning algorithm, attempting to give each
        process an equal weight.  If the global_items is a list, then all
        items are considered equally weighted.  For serial execution, this
        just returns the global list.

        @param global_items  If this is a list, then the weights of the items
                             are considered unity.  If this is a dictionary,
                             then the values in the dictionary are considered
                             weights.

        @param comm	     The communicator to partition across.  Default is 0 for serial mode.

        @param size	     The number of mpitasks that the tasks are to be 
                             partitioned across. Default is -1 for serial mode.

        @param rank          The rank of the mpitask that is calling this function.
			     Default is -1 for serial mode.

        @return A list containing a subset of the global items to be used
                on the current (local) processor
        '''
        if isinstance(global_items, list) or isinstance(global_items, set):
            return global_items
        elif isinstance(global_items, dict):
            return global_items.keys()
        else:
            err_msg = 'Global items object has unrecognized type (' \
                    + str(type(global_items)) + ')'
            raise TypeError(err_msg)

    def partition_across_comms(self, color, task_list):
        '''
        Partitions a task list across communicators so each member of the communicator
        recvs the same sublist to operate on.  Does nothing in serial mode.

        @param color      The group that this mpitask is part of.
  
        @param task_list  The list of tasks that will be partitioned across the communicators.

        @return task_list A list containing a subset of the global list that is to be used on 
                          the local mpitask.
        '''  
        return task_list


    def sync(self, comm=0):
        '''
        A wrapper on the MPI Barrier method.  Forces execution to wait for
        all other processors to get to this point in the code.  Does nothing
        in serial.

        @param comm  The communicator to sync. Default is 0 for serial mode.

        '''
        return

    def is_master(self, comm=0):
        '''
        Returns True or False depending on whether this rank is the master
        rank (i.e., rank 0).  In serial, always returns True.

        @param comm  The communicator to query.  Default is 0 for serial mode.

        @return True or False depending on whether this rank is the master
                rank (i.e., rank 0).
        '''
        return self._is_master

    def get_rank(self, comm=0):
        '''
        Returns the integer associated with the local MPI processor/rank.
        In serial, it always returns 0.

        @param comm  The communicator to query. Default is 0 for serial mode.

        @return The integer ID associated with the local MPI processor/rank
        '''
        return self._mpi_rank

    def get_size(self, comm=0):
        '''
        Returns the number of ranks in the MPI communicator.
        In serial, it always returns 1.

        @param comm  The communicator to query.  Default is 0 for serial mode.

        @return The integer number of ranks in the MPI communicator
        '''
        return self._mpi_size

    def sum(self, data, comm=0):
        '''
        This sums data across all processors.

        If the data is a dictionary (with assumed numberic values), then this
        summes the values associated with each key across all processors.  It
        returns a dictionary with the sum for each key.  Every processor
        must have the same keys in their associated dictionaries.

        If the data is not a dictionary, but is list-like (i.e., iterable),
        then this returns a single value with the sum of all values across all
        processors.

        If the data is not iterable (i.e., a single value), then it sums across
        all processors and returns one value.

        In serial, this returns just the sum on the local processor.

        @param data The data with values to be summed

        @param comm  The communicator to operate across.  Default is 0 for serial mode.

        @return The sum of the data values
        '''
        if (isinstance(data, dict)):
            totals = {}
            for name in data:
                totals[name] = self.sum(data[name])
            return totals
        elif (hasattr(data, '__len__')):
            return reduce(lambda x, y: x + y, data)
        else:
            return data

    def max(self, data, comm=0):
        '''
        This returns the maximum of the data across all processors.

        If the data is a dictionary (with assumed numberic values), then this
        find the maximum of the values associated with each key across all
        processors.  It returns a dictionary with the maximum for each key.
        Every processor must have the same keys in their associated
        dictionaries.

        If the data is not a dictionary, but is list-like (i.e., iterable),
        then this returns a single value with the maximum of all values across
        all processors.

        If the data is not iterable (i.e., a single value), then it finds the
        maximum across all processors and returns one value.

        In serial, this returns just the maximum on the local processor.

        @param data The data with values

        @param comm  The communicator to operate across.  Default is 0 for serial mode.

        @return The maximum of the data values
        '''
        if (isinstance(data, dict)):
            maxima = {}
            for name in data:
                maxima[name] = self.max(data[name])
            return maxima
        elif (hasattr(data, '__len__')):
            return max(data)
        else:
            return data

    def print_once(self, output, vlevel=0, comm=0):
        '''
        This method prints output to stdout, but only if it is the
        master processes and the verbosity level is high enough.

        @param output A string that should be printed to stdout

        @param vlevel The verbosity level associated with the message.  If
                      this level is less than the messenger's verbosity, no
                      output is generated.
       
        @param comm  The communicator to operate across.  Default is 0 for serial mode.

        '''
        if (self.is_master() and vlevel < self.verbosity):
            print output
            sys.stdout.flush()

    def print_all(self, output, vlevel=0, comm=0):
        '''
        This prints a message to stdout from every processor.

        @param output A string that should be printed to stdout

        @param vlevel The verbosity level associated with the message.  If
                      this level is less than the messenger's verbosity, no
                      output is generated.
        
        @param comm  The communicator to operate across.  Default is 0 for serial mode.
        '''
        if (vlevel < self.verbosity):
            ostr = '[' + str(self._mpi_rank) + '/' \
                       + str(self._mpi_size) + '] ' + output
            print ostr
            sys.stdout.flush()

    def Send_npArray(self, message, data, destination, comm):
        '''
        Wrapper around MPI calls to send a numPy array to another mpitask. Does 
        nothing in serial mode.

        @param message      A dictionary that contains: 1)'from_rank' 2)'shape' 3)'dtype'
                            These are used for handshaking and to initalize the numPy array
                            properly.

        @param data         The numPy array to send. 

        @param destination  The mpitask to send to.

        @param comm         The communicator that the message is being sent within.
        '''
        return

    def Recv_npArray(self, comm):
        '''
        Wrapper around MPI calls to recv a numPy array.  Doesn nothing in serial mode.

        @param comm  The communicator that the message is being recv was sent within.
        '''
        return

    def send_var_info(self, var_info, destination, comm):
        '''
        Wrapper around MPI call to send NetCDF variable information.  Does nothing in
        serial mode.
 
        @params var_info    A dictionary that contains the following NetCDF variable
                            information: 1)'varname' 2)'type_code' 3)'dim_names' 4)'attr'

        @params destination MPI task to send to.

        @params comm        The communicator that the message is being sent within.

        '''
        return

    def recv_var_info(self, comm):
        '''
        Wrapper around MPI calls to recv NetCDF variable information.  Doesn nothing in serial mode.

        @param comm  The communicator that the message is being recv was sent within.
        '''
        return

#==============================================================================
# MPIMessenger Class
#==============================================================================
class MPIMessenger(Messenger):
    '''
    This is the parallel-operation class for decomposition/parallel utilities.
    This is derived from the Messenger class, which defines the serial
    operation.  This defines operations using MPI.
    '''

    def __init__(self):
        '''
        Constructor
        '''

        ## Type of decomp utility constructed
        self.messenger_type = 'parallel'

        # Try to import the MPI module
        try:
            from mpi4py import MPI
        except:
            raise ImportError('Failed to import MPI.')

        ## Pointer to the MPI module
        self._mpi = MPI

        ## The rank of the processor
        self._mpi_rank = self._mpi.COMM_WORLD.Get_rank()

        ## MPI Communicator size
        self._mpi_size = self._mpi.COMM_WORLD.Get_size()

        ## Whether this is the master process/rank
        self._is_master = (self._mpi_rank == 0)

    def split_comm(self, rank, list_size, comm_size=-99, comm=-99):
        '''
        Splits the given communicator into subcommunicators.  Does
        nothing in serial.

        @param rank           The rank of the mpitask that is calling this function.
 
        @param list_size      The total number of tasks that need to be performed.

        @param comm_size  The minimum number of mpitasks per subcommunicator.
                              Default is the size of COMM_WORLD.

        @param comm           The parent comminucator to split from.  Default is COMM_WORLD.

        @return intercomm     The new subcommincator that this rank is part of.

        @return color         Which group this rank is part of. 
        '''
        if (comm_size == -99):
            comm_size = self._mpi_size
        if (comm == -99):
            comm = self._mpi.COMM_WORLD
        color = (rank//comm_size) % list_size
        intercomm = comm.Split(color,rank)

        return intercomm,color

    def partition(self, global_items, comm=-99, size=-99, rank=-99):
        '''
        Given a container of items, this algorithm selects a subset of
        items to be used by the local process.  If the 'global_items' object
        is a dictionary, then the values of the dictionary are treated as
        weights for the partitioning algorithm, attempting to give each
        process an equal weight.  If the global_items is a list, then all
        items are considered equally weighted.  For serial execution, this
        just returns the global list.

        @param global_items  If this is a list, then the weights of the items
                             are considered unity.  If this is a dictionary,
                             then the values in the dictionary are considered
                             weights.

        @param comm          The communicator to partition across. Default is COMM_WORLD.

        @param size          The number of mpitasks that the tasks are to be 
                             partitioned across. Default is the size of COMM_WORLD.

        @param rank          The rank of the mpitask that is calling this function.
                             Default is the rank within COMM_WORLD.

        @return A list containing a subset of the global items to be used
                on the current (local) processor
        '''
        if (size == -99):
            size = self._mpi_size
        if (comm == -99):
            comm = self._mpi.COMM_WORLD
        if (rank == -99):
            rank = self._mpi_rank
        if isinstance(global_items, list) or isinstance(global_items, set):
            global_dict = dict((name, 1) for name in global_items)
        elif isinstance(global_items, dict):
            global_dict = global_items
        else:
            err_msg = 'Global items object has unrecognized type (' \
                    + str(type(global_items)) + ')'
            raise TypeError(err_msg)

        # Sort the names of the variables by their weight
        global_list = list(zip(*sorted(global_dict.items(), key=lambda p: p[1]))[0])

        # KMP: A better partitioning algorithm should be implemented.  The
        #      above line with the striding below does not necessarily load
        #      balance as well as could be done.  It is easy, though...

        # Return a subset of the list by striding though the list
        return global_list[rank::size]

    def partition_across_comms(self, color, task_list):
        '''
        Partitions a task list across communicators so each member of the communicator
        recvs the same sublist to operate on.  Does nothing in serial mode.

        @param color      The group that this mpitask is part of.
  
        @param task_list  The list of tasks that will be partitioned across the communicators.

        @return task_list A list containing a subset of the global list that is to be used on 
                          the local mpitask.
        '''  
        n_tasks = len(task_list)

        comm_count = self.max(color)+1
        llen = int(math.floor(n_tasks//comm_count))
        rem = n_tasks - llen * comm_count
        istart = list(range(0,comm_count))
        iend = list(range(0,comm_count))
        istart[0] = 0
        if 0 <= rem-1:
            iend[0] = llen + 1
        else:
            iend[0] = llen
        for i in range(1,color+1):
            istart[i] = iend[i-1]
            if i <= rem - 1:
                iend[i] = istart[i] + llen + 1
            else:
                iend[i] = istart[i] + llen

        l_task_list = [task_list[i] for i in range(istart[color], iend[color])]

        return l_task_list


    def sync(self, comm=-99):
        '''
        A wrapper on the MPI Barrier method.  Forces execution to wait for
        all other processors to get to this point in the code.

        @param comm  The communicator to sync.  Default is COMM_WORLD.

        '''
        if (comm == -99):
            comm = self._mpi.COMM_WORLD
        comm.Barrier()

    def is_master(self, comm=-99):
        '''
        Returns True or False depending on whether this rank is the master
        rank (i.e., rank 0).  In serial, always returns True.

        @param comm  The communicator to query. Default is COMM_WORLD.

        @return True or False depending on whether this rank is the master
                rank (i.e., rank 0).
        '''
        if (comm == -99):
            comm = self._mpi.COMM_WORLD
        rank = comm.Get_rank()
        return (rank == 0)

    def get_rank(self, comm=-99):
        '''
        Returns the integer associated with the local MPI processor/rank.
        In serial, it always returns 0.

        @param comm  The communicator to query. Default is COMM_WORLD.

        @return The integer ID associated with the local MPI processor/rank
        '''
        if (comm == -99):
            comm = self._mpi.COMM_WORLD
        return comm.Get_rank()

    def get_size(self, comm=-99):
        '''
        Returns the number of ranks in the MPI communicator.
        In serial, it always returns 1.

        @param comm  The communicator to query.  Default is COMM_WORLD.

        @return The integer number of ranks in the MPI communicator
        '''
        if (comm == -99):
            comm = self._mpi.COMM_WORLD
        return comm.Get_size()

    def sum(self, data, comm=-99):
        '''
        This sums data across all processors.

        If the data is a dictionary (with assumed numberic values), then this
        summes the values associated with each key across all processors.  It
        returns a dictionary with the sum for each key.  Every processor
        must have the same keys in their associated dictionaries.

        If the data is not a dictionary, but is list-like (i.e., iterable),
        then this returns a single value with the sum of all values across all
        processors.

        If the data is not iterable (i.e., a single value), then it sums across
        all processors and returns one value.

        In serial, this returns just the sum on the local processor.

        @param data The data with values to be summed

        @param comm  The communicator to operate across.  Default is COMM_WORLD.

        @return The sum of the data values
        '''
        if (comm == -99):
            comm = self._mpi.COMM_WORLD
        if (isinstance(data, dict)):
            totals = {}
            for name in data:
                totals[name] = self.sum(data[name])
            return totals
        elif (hasattr(data, '__len__')):
            total = Messenger.sum(self, data)
            return self.sum(total)
        else:
            return comm.allreduce(data, op=self._mpi.SUM)

    def max(self, data, comm=-99):
        '''
        This returns the maximum of the data across all processors.

        If the data is a dictionary (with assumed numberic values), then this
        find the maximum of the values associated with each key across all
        processors.  It returns a dictionary with the maximum for each key.
        Every processor must have the same keys in their associated
        dictionaries.

        If the data is not a dictionary, but is list-like (i.e., iterable),
        then this returns a single value with the maximum of all values across
        all processors.

        If the data is not iterable (i.e., a single value), then it finds the
        maximum across all processors and returns one value.

        In serial, this returns just the maximum on the local processor.

        @param data The data with values

        @param comm  The communicator to operate across.  Default is COMM_WORLD.

        @return The maximum of the data values
        '''
        if (comm == -99):
            comm = self._mpi.COMM_WORLD
        if (isinstance(data, dict)):
            maxima = {}
            for name in data:
                maxima[name] = self.max(data[name])
            return maxima
        elif (hasattr(data, '__len__')):
            maximum = Messenger.max(self, data)
            return self.max(maximum)
        else:
            return comm.allreduce(data, op=self._mpi.MAX)

    def Send_npArray(self, message, data, destination, comm):
        '''
        Wrapper around MPI calls to send a numPy array to another mpitask. Does 
        nothing in serial mode.

        @param message      A dictionary that contains: 1)'from_rank' 2)'shape' 3)'dtype'
                            4) 'name'
                            These are used for handshaking and to initalize the numPy array
                            properly.

        @param data         The numPy array to send. 

        @param destination  The mpitask to send to.

        @param comm         The communicator that the message is being sent within.
        '''
        # Sends a numPy array to the communicator's root
        comm.send(message,dest=destination,tag=77)
        ack = comm.recv(source=destination,tag=88)
        if message['shape']:
            comm.Send(data,dest=destination,tag=99)
        else:
            comm.send(data,dest=destination,tag=99)       

    def Recv_npArray(self, comm):
        '''
        Wrapper around MPI calls to recv a numPy array.  Doesn nothing in serial mode.

        @param comm      The communicator that the message is being recv was sent within.

        @return name     Returns the 'name' identifier it recved.

        @return np_array Returns the numPy array it recved.
        '''
        #Root Only: Receive a numPy array
        message = {}
        message = comm.recv(source=MPI.ANY_SOURCE,tag=77)
        comm.send("Recieved request",dest=message['from_rank'],tag=88)
        if message['shape']:
            np_array = np.ones((message['shape']),dtype=message['dtype'])
            comm.Recv(np_array,source=message['from_rank'],tag=99)
        else:
            np_array = comm.recv(source=message['from_rank'],tag=99)

        return message['name'],np_array

    def send_var_info(self, var_info, destination, comm):
        '''
        Wrapper around MPI call to send NetCDF variable information.  Does nothing in
        serial mode.
 
        @params var_info    A dictionary that contains the following NetCDF variable
                            information: 1)'varname' 2)'type_code' 3)'dim_names' 4)'attr'

        @params destination MPI task to send to.

        @params comm        The communicator that the message is being sent within.

        '''
        comm.send(var_info,dest=destination,tag=55)

    def recv_var_info(self, comm):
        '''
        Wrapper around MPI calls to recv NetCDF variable information.  Doesn nothing in serial mode.

        @param comm        The communicator that the message is being recv was sent within.

        @returns var_info  Returns the NetCDF variable information that it recved.
        '''
        var_info = comm.recv(source=MPI.ANY_SOURCE,tag=55)
        return var_info
