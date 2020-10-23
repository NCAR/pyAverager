#!/usr/bin/env python

from pyaverager import PyAverager, specification
import os

#### User modify ####

in_dir='tests/data/series_files/ocn/'
out_dir= 'tests/output/PyAverager/ocn/series/'
pref= 'test_data.pop.h'
htype= 'series'
average = ['tavg:1:5','mavg:1:5','moc:1:5','mocm:1:5','hor.meanConcat:1:5']
wght= False
ncfrmt = 'netcdf'
serial=False

var_list = ['TEMP', 'SALT']
mean_diff_rms_obs_dir = 'tests/data/timeseries_obs/'
region_nc_var = 'REGION_MASK'
regions={1:'ocean'}
region_wgt_var = 'TAREA'
obs_dir = 'tests/data/timeseries_obs/'
obs_file = 'obs.nc'
reg_obs_file_suffix = '_hor_mean_obs.nc'
vertical_levels = 4

clobber = True
suffix = 'nc'
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
                                  varlist=var_list,
                                  serial=serial,
                                  clobber=clobber,
                                  mean_diff_rms_obs_dir=mean_diff_rms_obs_dir,
                                  region_nc_var=region_nc_var,
                                  regions=regions,
                                  region_wgt_var=region_wgt_var,
                                  obs_dir=obs_dir,
                                  obs_file=obs_file,
                                  reg_obs_file_suffix=reg_obs_file_suffix,
                                  vertical_levels=vertical_levels)

PyAverager.run_pyAverager(pyAveSpecifier)

