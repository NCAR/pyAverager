#!/usr/bin/env python

from pyaverager import PyAverager, specification

#### User modify ####

in_dir = 'tests/data/slice_files/atm/'
out_dir = 'tests/output/PyAverager//atm/slice/'
pref = 'test_data.cam.h0'
htype = 'slice'
average = [
    'dep_ann:1:4',
    'djf:1:4',
    'dep_mam:1:4',
    'dep_jja:1:4',
    'dep_son:1:4',
    'zonalavg:1:4',
    'jan:1:4',
    'feb:1:4',
    'mar:1:4',
    'apr:1:4',
    'may:1:4',
    'jun:1:4',
    'jul:1:4',
    'aug:1:4',
    'sep:1:4',
    'oct:1:4',
    'nov:1:4',
    'dec:1:4',
]
wght = True
ncfrmt = 'netcdf'
serial = False
suffix = 'nc'
clobber = True
date_pattern = 'yyyymm-yyyymm'

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
    clobber=clobber,
)

PyAverager.run_pyAverager(pyAveSpecifier)
