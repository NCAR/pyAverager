#!/usr/bin/env python

from pyaverager import PyAverager, specification
import os

#### User modify ####

in_dir='tests/data/slice_files/lnd/'
out_dir= 'tests/output/PyAverager/lnd/slice/'
pref= 'test_data.clm.h0'
htype= 'slice'
average= ['mons:1:5','dep_ann:1:5','dep_mam:1:5','dep_jja:1:5','dep_son:1:5','annall:1:5']
wght= True
ncfrmt = 'netcdf'
serial=False
suffix = 'nc'
clobber = True
date_pattern= 'yyyymm-yyyymm'

#### End user modify ####

pyAveSpecifier = specification.create_specifier(in_directory=in_dir,
			          out_directory=out_dir,
				  prefix=pref,
                                  suffix=suffix,
                                  date_pattern=date_pattern,
				  hist_type=htype,
				  avg_list=average,
				  weighted=wght,
				  ncformat=ncfrmt,
				  serial=serial,
                                  clobber=clobber)

PyAverager.run_pyAverager(pyAveSpecifier)

