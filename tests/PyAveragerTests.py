from __future__ import print_function

import unittest
import pytest
from subprocess import Popen, PIPE



@pytest.mark.parametrize('n', [4])
@pytest.mark.parametrize('spec',['tests/PyAverager_tests/control_atm_series.py', 
                                 'tests/PyAverager_tests/control_atm_slice.py',
                                 'tests/PyAverager_tests/control_lnd_series.py',      
                                 'tests/PyAverager_tests/control_lnd_slice.py',
                                 'tests/PyAverager_tests/control_ice_series.py',      
                                 'tests/PyAverager_tests/control_ice_slice.py',
                                ])
def test_cli_mpi(n, spec):

    p_run = Popen('mpirun -n 4 coverage run -p '+spec, stdout=PIPE, stderr=PIPE,shell=True)
    out,err = p_run.communicate()
    print('---------------------')
    print(out)
    print(err)
    print('---------------------')
    assert p_run.returncode == 0


 



