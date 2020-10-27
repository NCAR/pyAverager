#!/usr/bin/env python

from pyaverager import PyAverager, specification

#### User modify ####

in_dir = 'tests/data/slice_files/ice/'
out_dir = 'tests/output/PyAverager/ice/slice/'
pref = 'test_data.cice.h'
htype = 'slice'
average = [
    'ya:1',
    'ya:2',
    'ya:3',
    'ya:4',
    'ya:5',
    'dep_jfm:1:5',
    'dep_fm:1:5',
    'dep_amj:1:5',
    'dep_jas:1:5',
    'dep_ond:1:5',
    'dep_on:1:5',
]
wght = False
ncfrmt = 'netcdf'
serial = False

suffix = 'nc'
date_pattern = 'yyyymm-yyyymm'
clobber = True

ice_obs_file = 'tests/data/ice_obs/gx1v6_grid.nc'
reg_file = 'tests/data/ice_obs/REGION_MASK.nc'
year0 = 1
year1 = 5
ncl_location = 'pyaverager/'

#### End user modify ####

pyAveSpecifier = specification.create_specifier(
    in_directory=in_dir,
    out_directory=out_dir,
    prefix=pref,
    suffix=suffix,
    date_pattern=date_pattern,
    hist_type=htype,
    avg_list=average,
    weighted=wght,
    ncformat=ncfrmt,
    serial=serial,
    ice_obs_file=ice_obs_file,
    reg_file=reg_file,
    year0=year0,
    year1=year1,
    clobber=clobber,
    ncl_location=ncl_location,
)

PyAverager.run_pyAverager(pyAveSpecifier)
