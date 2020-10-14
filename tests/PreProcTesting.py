from __future__ import print_function

import unittest
import pytest
from subprocess import Popen

from pyaverager import PyAverager, specification, PreProc


average = ['ya:1', 'ya:2', 'ya:3', 'ya:4', 'ya:5', 'dep_jfm:1:5','dep_fm:1:5','dep_amj:1:5','dep_jas:1:5','dep_ond:1:5','dep_on:1:5']
wght= False
ncfrmt = 'netcdf'
serial=False
clobber = True

ice_obs_file = 'tests/data/gx1v6_grid.nc'
reg_file ='tests/data/REGION_MASK.nc'

year0 = 1
year1 = 5

ncl_location = 'pyaverager/'

pyAveSpecifier_slice = specification.create_specifier(
                                  in_directory='tests/data/slice_files/ice/',
                                  out_directory='tests/output/Preproc/',
                                  prefix='test_data.cice.h',
                                  suffix='nc',
                                  date_pattern='yyyy-mm',
                                  hist_type='slice',
                                  avg_list=average,
                                  weighted=wght,
                                  ncformat=ncfrmt,
                                  serial=serial,
                                  ice_obs_file=ice_obs_file,
                                  reg_file=reg_file,
                                  year0=year0,
                                  year1=year1,
                                  clobber=clobber,
                                  ncl_location=ncl_location)

pyAveSpecifier_series = specification.create_specifier(
                                  in_directory='tests/data/series_files/ice/',
                                  out_directory='tests/output/Preproc/',
                                  prefix='test_data.cice.h',
                                  suffix='nc',
                                  date_pattern='yyyymm-yyyymm',
                                  hist_type='series',
                                  avg_list=average,
                                  weighted=wght,
                                  ncformat=ncfrmt,
                                  serial=serial,
                                  ice_obs_file=ice_obs_file,
                                  reg_file=reg_file,
                                  year0=year0,
                                  year1=year1,
                                  clobber=clobber,
                                  ncl_location=ncl_location)



@pytest.mark.parametrize('n', [4])
@pytest.mark.parametrize('spec',['tests/Preproc_Specifier_slice.py', 'tests/Preproc_Specifier_series.py'])
def test_cli_mpi(n, spec):

    pre_cmds = ['coverage', 'run', '-p']
    mpirun = ['mpirun', '-n', str(n)] if n > 0 else []
    run_cmds = mpirun + pre_cmds + [spec] 
    print (run_cmds) 
    p_run = Popen(run_cmds)
    p_run.communicate()
    assert p_run.returncode == 0


 



