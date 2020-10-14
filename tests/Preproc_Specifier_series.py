#! /usr/bin/env python

import os

print(os.getcwd())

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

PreProc.run_pre_proc(pyAveSpecifier_series)
