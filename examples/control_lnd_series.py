#!/usr/bin/env python

import specification
import PyAverager

#### User modify ####

in_dir='/glade/u/tdd/asap/data/b.e12.B1850C5CN.ne30_g16.init.ch.027/lnd/mon/tseries/'
out_dir= '/glade/scratch/mickelso/averager_sandbox/results/lnd/series/'
pref= 'b.e12.B1850C5CN.ne30_g16.init.ch.027.clm2.h0'
fp= 'prefix*-*.nc'
htype= 'series'
average= ['dep_ann:1:10','dep_mam:1:10','dep_jja:1:10','dep_son:1:10',
            'jan:1:10','feb:1:10','mar:1:10','apr:1:10','may:1:10','jun:1:10',
            'jul:1:10','aug:1:10','sep:1:10','oct:1:10','nov:1:10','dec:1:10']
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

