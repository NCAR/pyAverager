from __future__ import print_function

import pytest

import pyaverager
from pyaverager import specification


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


def test_pyAveragerSpecifier_slice():

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
    assert type(pyAveSpecifier_slice) ==  pyaverager.specification.pyAveragerSpecifier 


def test_pyAveragerSpecifier_series():

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
    assert type(pyAveSpecifier_series) == pyaverager.specification.pyAveragerSpecifier


def test_pyAveragerSpecifier_series_split():

    pyAveSpecifier_series = specification.create_specifier(
                                  in_directory='tests/data/series_files/ice/',
                                  out_directory='tests/output/Preproc/',
                                  prefix='test_data.cice.h',
                                  suffix='nc',
                                  date_pattern='yyyymm-yyyymm',
                                  hist_type='series',
                                  avg_list=average,
                                  weighted=wght,
                                  split = True,
                                  split_files = 'nh,sh',
                                  split_orig_size = 'nj=384,ni=320',
                                  ncformat=ncfrmt,
                                  serial=serial,
                                  ice_obs_file=ice_obs_file,
                                  reg_file=reg_file,
                                  year0=-99,
                                  year1=-99,
                                  clobber=clobber,
                                  ncl_location=ncl_location)
    assert type(pyAveSpecifier_series) == pyaverager.specification.pyAveragerSpecifier
