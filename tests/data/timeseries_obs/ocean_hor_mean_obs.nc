CDF       
      z_t             history      Wed Oct 21 14:36:28 2020: ncks -d z_t,1,4 /Users/mickelso/Desktop/pyaverager/tests/data/timeseries_obs/ocean_hor_mean_obs.nc /Users/mickelso/Desktop/pyaverager/tests/data/timeseries_obs/ocean_hor_mean_obs_smaller.nc
Wed Oct 21 13:28:09 2020: ncrename -v SALT,var02 ocean_hor_mean_obs.nc ocean_hor_mean_obs.nc
Wed Oct 21 13:27:41 2020: ncrename -v TEMP,var01 ocean_hor_mean_obs.nc ocean_hor_mean_obs.nc
Tue Feb 24 13:19:04 2015: ncwa -m REGION_MASK -T eq -M 2 -w TAREA -a nlon,nlat -v TEMP,SALT obs.nc Pac_hor_mean_obs.nc
Tue Feb 24 13:19:04 2015: ncatted -a _FillValue,TLONG,d,, obs.nc
Tue Feb 24 13:19:04 2015: ncatted -a _FillValue,TLAT,d,, obs.nc
Tue Feb 24 13:19:04 2015: ncatted -a missing_value,TLONG,d,, obs.nc
Tue Feb 24 13:19:04 2015: ncatted -a missing_value,TLAT,d,, obs.nc
Tue Feb 24 13:19:04 2015: ncatted -a _FillValue,SALT,c,f,-99. obs.nc
Tue Feb 24 13:19:04 2015: ncatted -a _FillValue,TEMP,c,f,-99. obs.nc
Tue Feb 24 13:19:03 2015: ncrename -O -d X,nlon -d Y,nlat -d depth,z_t obs.nc
Tue Feb 24 13:19:03 2015: ncks -A -v TAREA,REGION_MASK /glade/scratch/mickelso/averager_sandbox/obs//b.e12.B1850C5CN.ne30_g16.init.ch.027.pop.h.0001.nc obs.nc
Tue Feb 24 13:19:03 2015: ncks -A -v SALT SALT_obs.nc obs.nc
Fri Feb 13 10:26:02 2009: ncwa -a time PHC2_TEMP_gx1v6.nc PHC2_TEMP_gx1v6_ann_avg.nc      nco_openmp_thread_number            NCO       `netCDF Operators version 4.9.5 (Homepage = http://nco.sf.net, Code = http://github.com/nco/nco)          var01                   	long_name         Potential Temperature      units         	degrees C      missing_value         ��     coordinates       TLONG TLAT depth time      
_FillValue        ��     cell_methods      nlat, nlon: mean        �   var02                   	long_name         Salinity   units         psu    missing_value         ��     coordinates       TLONG TLAT depth time      
_FillValue        ��     cell_methods      nlat, nlon: mean        A�_!A��
A�C�A��B
sFB
��B
�$B
�