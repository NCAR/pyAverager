from __future__ import print_function

import unittest
import pytest
from subprocess import Popen, PIPE

from pyaverager import PyAverager, specification, PreProc




@pytest.mark.parametrize('n', [4])
@pytest.mark.parametrize('spec',['tests/PreProc_tests/Preproc_Specifier_slice.py', 'tests/PreProc_tests/Preproc_Specifier_series.py'])
def test_cli_mpi(n, spec):

    p_run = Popen('mpirun -n 4 coverage run -p '+spec, stdout=PIPE, stderr=PIPE,shell=True)
    out,err = p_run.communicate()
    print('---------------------')
    print(out)
    print(err)
    print('---------------------')
    assert p_run.returncode == 0


 



