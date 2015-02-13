#!/usr/bin/env python

import specification
import PyAverager

#### User modify ####

in_dir='/glade/u/tdd/asap/data/b.e12.B1850C5CN.ne30_g16.init.ch.027/ice/hist/'
out_dir= '/glade/scratch/mickelso/averager_sandbox/results/ice/slice/'
pref= 'b.e12.B1850C5CN.ne30_g16.init.ch.027.cice.h'
fp= 'prefix*-*.nc'
htype= 'slice'
average= ['ya:1', 'ya:2', 'ya:3', 'ya:4', 'ya:5', 'ya:6', 'ya:7', 'ya:8', 'ya:9', 'ya:10',
            'jfm:1:10','fm:1:10','amj:1:10','jas:1:10','ond:1:10','on:1:10']
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

