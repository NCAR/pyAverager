import netCDF4 as nc
import numpy as np

ml = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

casename = 'test_data.'
comps={'atm':'cam.h0', 'ice':'cice.h', 'ocn':'pop.h'}
tseries_date = '000101-000512.nc'
lat = np.arange(20, dtype=float)
lon = np.arange(40, dtype=float)
lev = np.arange(4, dtype=float)

vnm = []
for v in range(1,11):
    vnm.append("var"+str(v).zfill(2))
vnm.append('hi')
vnm.append('aice')
vnm.append('aice_nh')
vnm.append('aice_sh')
vnm.append('REGION_MASK')
vnm.append('TAREA')

# Create time slice files
for comp in comps.keys():
    basename = casename+comps[comp]
    for y in range(1,6):
        year = str(y).zfill(4)
        for m in range(1,13):
            month = str(m).zfill(2)

            slice_out_file = nc.Dataset('slice_files/'+comp+'/'+basename+'.'+year+'-'+month+'.nc', 'w')

            slice_out_file.createDimension("time", None)
            slice_out_file.createDimension("lat", lat.size)
            slice_out_file.createDimension("lon", lon.size)
            slice_out_file.createDimension("lev", lev.size)

            var_list = []

            time_o = slice_out_file.createVariable("time", "f4", ("time"))
            time_o.setncatts({"units": "days since 0001-01-01 00:00:00"})
            lev_o = slice_out_file.createVariable("lev", "f4", ("lev"))
            lev_o.setncatts({"short_name": "level"})
            lat_o = slice_out_file.createVariable("lat", "f4", ("lat"))
            lat_o.setncatts({"short_name": "latitude"})
            lon_o = slice_out_file.createVariable("lon", "f4", ("lon"))
            lon_o.setncatts({"stort_name": "longitude"})

            for v,name in enumerate(vnm):
                if "REGION_MASK" not in name and "TAREA" not in name:
                    if (v % 2) == 0 and 'aice' not in name:
                        var_list.append(slice_out_file.createVariable(name, "f4", ("time", "lat", "lon")))
                    else:
                        var_list.append(slice_out_file.createVariable(name, "f4", ("time", "lev", "lat", "lon"), fill_value=1.0e36))
            if 'ocn' in comp:
                var_list.append(slice_out_file.createVariable("REGION_MASK", "i", ("lat", "lon")))
                var_list.append(slice_out_file.createVariable("TAREA", "f4", ("lat", "lon")))

            time_o[:] = ((y-1)*365) + ml[m-1]
            lev_o[:] = lev
            lat_o[:] = lat
            lon_o[:] = lon
            
            for v,name in enumerate(vnm):
                if "REGION_MASK" in name:
                    if 'ocn' in comp:
                        a = np.empty([lat.size,lon.size], dtype=int)
                        a.fill(1)
                        var_list[v][:] = a
                elif "TAREA" in name:
                    if 'ocn' in comp:
                        a = np.empty([lat.size,lon.size], dtype=int)
                        area = 6883082761548.54
                        a.fill(area)
                        var_list[v][:] = a 
                elif (v % 2) == 0 and 'aice' not in name:
                    a = np.empty([1,lat.size,lon.size], dtype=float)
                    a.fill(m) 
                    var_list[v][:] = a
                else:
                    a = np.empty([1,lev.size,lat.size,lon.size], dtype=float)
                    a.fill(m)
                    var_list[v][:] = a
                


            slice_out_file.close()

        
# Create time series files
values = {}
for m in range(1,13):
    values[m] = np.empty([1,lat.size,lon.size], dtype=float)
    values[m].fill(m)
time_v = []
for y in range(1,6):
    for m in range(1,13):
        time_v.append(((y-1)*365) + ml[m-1])

for comp in comps.keys():
    basename = casename+comps[comp]
    for v,name in enumerate(vnm):
        series_out_file = nc.Dataset('series_files/'+comp+'/'+basename+"."+name+"."+tseries_date, "w")

        if '_nh' in name:
            name = name.replace('_nh', '')
        if '_sh' in name:                   
            name = name.replace('_sh', '')                 
        series_out_file.createDimension("time", None)
        series_out_file.createDimension("lat", lat.size)
        series_out_file.createDimension("lon", lon.size)
        series_out_file.createDimension("lev", lev.size)

        time_o = slice_out_file.createVariable("time", "f4", ("time"))
        time_o.setncatts({"units": "days since 0001-01-01 00:00:00"})
        lev_o = slice_out_file.createVariable("lev", "f4", ("lev"))
        lev_o.setncatts({"short_name": "level"})
        lat_o = slice_out_file.createVariable("lat", "f4", ("lat"))
        lat_o.setncatts({"short_name": "latitude"})
        lon_o = slice_out_file.createVariable("lon", "f4", ("lon"))
        lon_o.setncatts({"stort_name": "longitude"})

        if (v % 2) == 0 and 'aice' not in name:
            var = series_out_file.createVariable(name, "f4", ("time", "lat", "lon"), fill_value=1.0e36)
        else:
            var = series_out_file.createVariable(name, "f4", ("time", "lev", "lat", "lon"), fill_value=1.0e36)

        time_o[:] = time_v 
        lev_o[:] = lev
        lat_o[:] = lat
        lon_o[:] = lon

        if (v % 2) == 0 and 'aice' not in name:
            a = np.empty([60,lat.size,lon.size], dtype=float)
        else:
            a = np.empty([60,lev.size,lat.size,lon.size], dtype=float)
        if v < 10:
            i=0
            for y in range(1,6):
                for m in range(1,13):
                    a[i,:] = m
                    i += 1
        var[:] = a

        series_out_file.close()
