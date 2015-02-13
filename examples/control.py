#!/usr/bin/env python

import specification
import PyAverager

#### User modify ####

in_dir='/glade/u/tdd/asap/data/b40.20th.track1.1deg.006/atm/mon/tseries/'
out_dir= '/glade/scratch/mickelso/averager_sandbox/results/atm/series/'
pref= 'b40.20th.track1.1deg.006.cam2.h0'
fp= 'prefix*-*.nc'
htype= 'series'
average= ['ya:1850', 'ya:1851', 'ya:1852', 'ya:1853', 'ya:1854', 'ya:1855', 'ya:1856', 'ya:1857', 'ya:1858', 'ya:1859',
            'dep_ann:1851:1858','dep_djf:1850:1858','dep_mam:1850:1859','dep_jja:1850:1859','dep_son:1850:1859',
            'jan:1850:1859','feb:1850:1859','mar:1850:1859','apr:1850:1859','may:1850:1859','jun:1850:1859',
            'jul:1850:1859','aug:1850:1859','sep:1850:1859','oct:1850:1859','nov:1850:1859','dec:1850:1859',
	    'dep_tavg:1850:1859','dep_mavg:1850']
wght= False
spl= False
split_fn= 'null'
split_size= 'lon=288,lat=192'
ncfrmt = 'netcdf'
var_list = ['T','TS','UU']
serial=False

#### End user modify ####

pyAveSpecifier = specification.create_specifier(in_directory=in_dir,
			          out_directory=out_dir,
				  prefix=pref,
				  file_pattern=fp,
				  hist_type=htype,
				  avg_list=average,
				  weighted=wght,
				  split=spl,
				  split_files=split_fn,
				  split_orig_size=split_size,
				  ncformat=ncfrmt,
				  varlist=var_list,
				  serial=serial)

PyAverager.run_pyAverager(pyAveSpecifier)

