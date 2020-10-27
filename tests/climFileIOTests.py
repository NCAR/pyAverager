from __future__ import print_function

import pytest

from pyaverager import climFileIO
import netCDF4 as nc

test_filename = 'tests/data/slice_files/ice/test_data.cice.h.0001-01.nc'
test_file = nc.Dataset(test_filename, "r")

series_hist_dict = {
    1: {
        0: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 1,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 2,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 3,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 4,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 5,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 6,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 7,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 8,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 9,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 10,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 11,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    2: {
        0: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 12,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 13,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 14,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 15,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 16,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 17,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 18,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 19,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 20,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 21,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 22,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 23,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    3: {
        0: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 24,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 25,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 26,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 27,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 28,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 29,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 30,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 31,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 32,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 33,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 34,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 35,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    4: {
        0: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 36,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 37,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 38,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 39,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 40,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 41,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 42,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 43,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 44,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 45,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 46,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 47,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    5: {
        0: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 48,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 49,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 50,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 51,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 52,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 53,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 54,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 55,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 56,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 57,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 58,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/series_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 59,
            'date_stamp': '000101-000512',
            'pattern': ['$prefix', '.', '$var', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    6: {},
}

slice_hist_dict = {
    1: {
        0: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-01',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-02',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-03',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-04',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-05',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-06',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-07',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-08',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-09',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-10',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-11',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0001-12',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    2: {
        0: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-01',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-02',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-03',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-04',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-05',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-06',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-07',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-08',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-09',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-10',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-11',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0002-12',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    3: {
        0: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-01',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-02',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-03',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-04',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-05',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-06',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-07',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-08',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-09',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-10',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-11',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0003-12',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    4: {
        0: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-01',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-02',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-03',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-04',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-05',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-06',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-07',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-08',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-09',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-10',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-11',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0004-12',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    5: {
        0: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-01',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        1: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-02',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        2: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-03',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        3: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-04',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        4: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-05',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        5: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-06',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        6: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-07',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        7: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-08',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        8: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-09',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        9: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-10',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        10: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-11',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
        11: {
            'directory': 'tests/data/slice_files/atm/',
            'fn': 'test_data.cam.h0',
            'index': 0,
            'date_stamp': '0005-12',
            'pattern': ['$prefix', '.', '$date_pattern', '$suffix'],
            'suffix': '.nc',
        },
    },
    6: {},
}


@pytest.mark.parametrize(
    'month_dict',
    [
        slice_hist_dict[1][0],
        slice_hist_dict[2][1],
        slice_hist_dict[3][2],
        slice_hist_dict[4][3],
        slice_hist_dict[5][4],
        series_hist_dict[1][6],
        series_hist_dict[2][7],
        series_hist_dict[3][8],
        series_hist_dict[4][9],
        series_hist_dict[5][10],
    ],
)
def test_open_file(month_dict):

    try_file = climFileIO.open_file('var01', month_dict, '', mess='True')
    assert type(test_file) == type(try_file)
    try_file.close()


@pytest.mark.parametrize(
    'hist_dict, months_to_average, years, ave_type, fyr, file_dict_len, open_list_len',
    [
        (slice_hist_dict, [11, 0, 1], [2, 3, 4], 'djf', 1, 4, 12),
        (slice_hist_dict, [11, 0, 1], [1, 2, 3, 4], 'djf', 1, 5, 15),
        (slice_hist_dict, [11, 0, 1], [2, 3, 4, 5], 'djf', 1, 5, 12),
        (slice_hist_dict, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [1, 2, 3, 4, 5], 'ann', 1, 5, 60),
        (series_hist_dict, [11, 0, 1], [2, 3, 4], 'djf', 1, 4, 1),
        (series_hist_dict, [11, 0, 1], [1, 2, 3, 4], 'djf', 1, 5, 1),
        (series_hist_dict, [11, 0, 1], [2, 3, 4, 5], 'djf', 1, 5, 1),
        (series_hist_dict, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], [1, 2, 3, 4, 5], 'ann', 1, 5, 1),
    ],
)
def test_open_and_close_all(
    hist_dict, months_to_average, years, ave_type, fyr, file_dict_len, open_list_len
):

    var = 'var02'
    split = ''
    depend = False
    file_dict, open_list = climFileIO.open_all_files(
        hist_dict, months_to_average, years, var, split, ave_type, depend, fyr
    )
    assert len(file_dict.keys()) == file_dict_len
    assert len(open_list) == open_list_len

    climFileIO.close_all_files(open_list)


def test_open_file_return_var():

    var_val = climFileIO.open_file_return_var(test_filename, 'var01')
    assert 800.0 == var_val.sum()


@pytest.mark.parametrize(
    'ave_type, result',
    [
        ('ya', 'test_data.cice.h.0001.nc'),
        ('tavg', 'tavg.0001.nc'),
        ('mavg', 'mavg.0001.nc'),
        ('hor.meanyr', 'atlantic_hor.meanyr.0001.nc'),
        ('hor.meanConcat', 'atlantic_hor_mean_hor.meanConcat.test_data.cice.h_0001.nc'),
    ],
)
def test_get_out_fn(ave_type, result):

    prefix = 'test_data.cice.h'
    date = '0001'
    suffix = 'nc'

    out_file_name = climFileIO.get_out_fn(ave_type, prefix, date, suffix, reg='atlantic')
    assert result == out_file_name


@pytest.mark.parametrize(
    'ncformat', ['netcdf4c', 'netcdf4c2', 'netcdf4', 'netcdf', 'netcdfLarge', 'foo']
)
def test_create_ave_file(ncformat):

    my_file = test_file
    outfile = 'tests/output/climFileIO/test_data.cice.h.0001.' + ncformat + '.nc'
    hist_string = 'test suite call'
    years = '0001'
    ncfile = climFileIO.create_ave_file(
        my_file, outfile, hist_string, ncformat, years, collapse_dim=''
    )
    assert type(test_file) == type(ncfile)
    ncfile.close()


def test_define_ave_file():

    l_master = True
    serial = True
    var_list = [
        'var01',
        'var02',
        'var03',
        'var04',
        'var05',
        'var06',
        'var07',
        'var08',
        'var09',
        'var10',
        'hi',
        'aice',
    ]
    lvar_list = [
        'var01',
        'var02',
        'var03',
        'var04',
        'var05',
        'var06',
        'var07',
        'var08',
        'var09',
        'var10',
        'hi',
        'aice',
    ]
    meta_list = ['lat', 'lon', 'lev']
    hist_dict = slice_hist_dict
    hist_type = 'slice'
    ave_descr = ['ya', '1']
    prefix = 'test_data.cice.h'
    outfile = 'test_data.cice.h.0001.nc'
    split = False
    split_name = ''
    out_dir = 'tests/output/climFileIO/'
    simplecomm = None
    nc_formt = 'netcdf4'
    month = 0
    key = 'var02'
    clobber = True
    firstYr = 1
    endYr = 1
    ave_date = '0001'

    all_files_vars, new_file = climFileIO.define_ave_file(
        l_master,
        serial,
        var_list,
        lvar_list,
        meta_list,
        hist_dict,
        hist_type,
        ave_descr,
        prefix,
        outfile,
        split,
        split_name,
        out_dir,
        simplecomm,
        nc_formt,
        month,
        key,
        clobber,
        firstYr,
        endYr,
        ave_date,
        pre_proc_attr=None,
        pre_proc_variables=None,
        collapse_dim='',
    )
    assert sorted(var_list + meta_list) == sorted(all_files_vars.keys())
    assert type(test_file) == type(new_file)
