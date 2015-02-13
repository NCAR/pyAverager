#!/usr/bin/env python

import specification
import PyAverager

#### User modify ####

in_dir='/glade/u/tdd/asap/data/b.e12.B1850C5CN.ne30_g16.init.ch.027/ocn/hist/'
out_dir= '/glade/scratch/mickelso/averager_sandbox/results/ocn/slice/'
pref= 'b.e12.B1850C5CN.ne30_g16.init.ch.027.pop.h'
fp= 'prefix*-*.nc'
htype= 'slice'
average= ['dep_tavg:1:10','dep_mavg:1:10']
wght= False
ncfrmt = 'netcdf'
serial=False

#### End user modify ####

pyAveSpecifier = specification.create_specifier(in_directory=in_dir,
			          out_directory=out_dir,
				  prefix=pref,
				  file_pattern=fp,
				  hist_type=htype,
				  avg_list=average,
				  weighted=wght,
				  ncformat=ncfrmt,
				  serial=serial)

PyAverager.run_pyAverager(pyAveSpecifier)

