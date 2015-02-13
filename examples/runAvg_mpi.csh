#!/bin/csh
#BSUB -n 160 
#BSUB -q regular
#BSUB -N 
#BSUB -W 4:00
#BSUB -R "span[ptile=8]"
#BSUB -P $YOUR_PORJECT
#BSUB -o pyAve.%J.out         # output file name in which %J is replaced by the job ID
#BSUB -e pyAve.%J.err         # error file name in which %J is replaced by the job ID

module load python 
module load all-python-libs

mpirun.lsf ./control_atm_series.py
mpirun.lsf ./control_atm_slice.py 

mpirun.lsf ./control_atm_se_series.py
mpirun.lsf ./control_atm_se_slice.py

mpirun.lsf ./control_ice_series.py
mpirun.lsf ./control_ice_slice.py

mpirun.lsf ./control_lnd_series.py
mpirun.lsf ./control_lnd_slice.py

mpirun.lsf ./control_ocn_series.py
mpirun.lsf ./control_ocn_slice.py

