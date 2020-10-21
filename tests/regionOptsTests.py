from __future__ import print_function

import pytest

from pyaverager import regionOpts

file_pattern = ['$prefix','.','$var','_','$hem','.','$date_pattern','.','$suffix']

def test_combine_regions():

    in_directory='tests/data/series_files/ice/'
    out_directory='tests/output/regionOpts/'

    fn1 = in_directory + '/test_data.cice.h.aice_nh.000101-000512.nc'
    fn2 = in_directory + '/test_data.cice.h.aice_sh.000101-000512.nc'
    outfile = out_directory + '/test_data.cice.h.aice.000101-000512.nc'

    dim1 = 'lat'
    dimlen1 = 60
    dim2 = 'lon'
    dimlen2 = 40
    split_dim = 'lat'

    clobber=True
  
#    regionOpts.combine_regions(fn1, fn2, outfile, dim1, dimlen1, dim2, dimlen2,  split_dim, clobber)
 
