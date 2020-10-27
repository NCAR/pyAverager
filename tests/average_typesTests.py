from __future__ import print_function

import pyaverager.average_types as ave_t


def test_average_compliance_correct():

    test_lists = {
        1: {
            'd': [
                'dep_ann:1:10',
                'dep_mam:1:10',
                'dep_jja:1:10',
                'dep_son:1:10',
                'zonalavg:1:10',
                'jan:1:10',
                'feb:1:10',
                'mar:1:10',
                'apr:1:10',
                'may:1:10',
                'jun:1:10',
                'jul:1:10',
                'aug:1:10',
                'sep:1:10',
                'oct:1:10',
                'nov:1:10',
                'dec:1:10',
            ],
            'rc': 0,
        },
        2: {
            'd': [
                'dep_ann:1850:1859',
                'djf:1850:1858',
                'dep_mam:1850:1859',
                'dep_jja:1850:1859',
                'dep_son:1850:1859',
                'zonalavg:1850:1859',
                'jan:1850:1859',
                'feb:1850:1859',
                'mar:1850:1859',
                'apr:1850:1859',
                'may:1850:1859',
                'jun:1850:1859',
                'jul:1850:1859',
                'aug:1850:1859',
                'sep:1850:1859',
                'oct:1850:1859',
                'nov:1850:1859',
                'dec:1850:1859',
            ],
            'rc': 0,
        },
        3: {
            'd': [
                'mons:1:10',
                'dep_ann:1:10',
                'dep_mam:1:10',
                'dep_jja:1:10',
                'dep_son:1:10',
                'annall:1:10',
            ],
            'rc': 0,
        },
        4: {
            'd': [
                'ya:1',
                'ya:2',
                'ya:3',
                'ya:4',
                'ya:5',
                'ya:6',
                'ya:7',
                'ya:8',
                'ya:9',
                'ya:10',
                'dep_jfm:1:10',
                'dep_fm:1:10',
                'dep_amj:1:10',
                'dep_jas:1:10',
                'dep_ond:1:10',
                'dep_on:1:10',
                'dep_tavg:1:10',
            ],
            'rc': 0,
        },
        5: {
            'd': ['tavg:1:10', 'mavg:1:10', 'moc:1:10', 'mocm:1:10', 'hor.meanConcat:1:10'],
            'rc': 0,
        },
    }

    for test_list in test_lists.keys():
        cm = ave_t.average_compliance(test_lists[test_list]['d'])
        assert cm is None


# def test_average_compliance_incorrect():
#
#    test_lists = {
#        1: {'d':['foo:1:10'], 'rc':1},
#        2: {'d':['dep_may:1850:1859'], 'rc':2},
#        3: {'d':['ya:1:10'], 'rc':3},
#        4: {'d':['dep_jfm:1'], 'rc':4},
#        5: {'d':['tavg:1:10:100'], 'rc':4},
#    }
#
#    for test_list in test_lists.keys():
#        with assertRaises(SystemExit) as cm:
#        ave_t.average_compliance(test_lists[test_list]['d'])
#        assert test_lists[test_list]['rc'] ==  cm.exception.code


def test_sort_depend():

    test_lists = {
        1: {
            0: [
                'dep_ann:1:10',
                'dep_mam:1:10',
                'dep_jja:1:10',
                'dep_son:1:10',
                'zonalavg:1:10',
                'jan:1:10',
                'feb:1:10',
                'mar:1:10',
                'apr:1:10',
                'may:1:10',
                'jun:1:10',
                'jul:1:10',
                'aug:1:10',
                'sep:1:10',
                'oct:1:10',
                'nov:1:10',
                'dec:1:10',
            ]
        },
        2: {
            0: [
                'dep_ann:1850:1859',
                'djf:1850:1858',
                'dep_mam:1850:1859',
                'dep_jja:1850:1859',
                'dep_son:1850:1859',
                'zonalavg:1850:1859',
                'jan:1850:1859',
                'feb:1850:1859',
                'mar:1850:1859',
                'apr:1850:1859',
                'may:1850:1859',
                'jun:1850:1859',
                'jul:1850:1859',
                'aug:1850:1859',
                'sep:1850:1859',
                'oct:1850:1859',
                'nov:1850:1859',
                'dec:1850:1859',
            ]
        },
        3: {
            0: [
                'mons:1:10',
                'dep_ann:1:10',
                'dep_mam:1:10',
                'dep_jja:1:10',
                'dep_son:1:10',
                'annall:1:10',
            ]
        },
        4: {
            0: [
                'ya:1',
                'ya:2',
                'ya:3',
                'ya:4',
                'ya:5',
                'ya:6',
                'ya:7',
                'ya:8',
                'ya:9',
                'ya:10',
                'dep_jfm:1:10',
                'dep_fm:1:10',
                'dep_amj:1:10',
                'dep_jas:1:10',
                'dep_ond:1:10',
                'dep_on:1:10',
            ]
        },
        5: {0: ['tavg:1:10', 'mavg:1:10', 'moc:1:10', 'mocm:1:10', 'hor.meanConcat:1:10']},
    }
    sorted_list = {
        1: {
            0: [
                'zonalavg:1:10',
                'jan:1:10',
                'feb:1:10',
                'mar:1:10',
                'apr:1:10',
                'may:1:10',
                'jun:1:10',
                'jul:1:10',
                'aug:1:10',
                'sep:1:10',
                'oct:1:10',
                'nov:1:10',
                'dec:1:10',
            ],
            1: ['ann:1:10:__d', 'mam:1:10:__d', 'jja:1:10:__d', 'son:1:10:__d'],
        },
        2: {
            0: [
                'djf:1850:1858',
                'zonalavg:1850:1859',
                'jan:1850:1859',
                'feb:1850:1859',
                'mar:1850:1859',
                'apr:1850:1859',
                'may:1850:1859',
                'jun:1850:1859',
                'jul:1850:1859',
                'aug:1850:1859',
                'sep:1850:1859',
                'oct:1850:1859',
                'nov:1850:1859',
                'dec:1850:1859',
                'prev_dec:1850:1858',
                'next_jan:1850:1858',
                'next_feb:1850:1858',
            ],
            1: ['ann:1850:1859:__d', 'mam:1850:1859:__d', 'jja:1850:1859:__d', 'son:1850:1859:__d'],
        },
        3: {
            0: [
                'mons:1:10',
                'annall:1:10',
                'oct:1:10',
                'apr:1:10',
                'sep:1:10',
                'mar:1:10',
                'dec:1:10',
                'nov:1:10',
                'jul:1:10',
                'aug:1:10',
                'feb:1:10',
                'jan:1:10',
                'may:1:10',
                'jun:1:10',
            ],
            1: ['ann:1:10:__d', 'mam:1:10:__d', 'jja:1:10:__d', 'son:1:10:__d'],
        },
        4: {
            0: [
                'ya:1',
                'ya:2',
                'ya:3',
                'ya:4',
                'ya:5',
                'ya:6',
                'ya:7',
                'ya:8',
                'ya:9',
                'ya:10',
                'oct:1:10',
                'aug:1:10',
                'apr:1:10',
                'jun:1:10',
                'dec:1:10',
                'mar:1:10',
                'may:1:10',
                'feb:1:10',
                'jul:1:10',
                'jan:1:10',
                'nov:1:10',
                'sep:1:10',
            ],
            1: [
                'jfm:1:10:__d',
                'fm:1:10:__d',
                'amj:1:10:__d',
                'jas:1:10:__d',
                'ond:1:10:__d',
                'on:1:10:__d',
            ],
        },
        5: {0: ['tavg:1:10', 'mavg:1:10', 'moc:1:10', 'mocm:1:10']},
    }

    for test_list in test_lists.keys():
        for i in range(1, 20):
            test_lists[test_list][i] = []
        cm = ave_t.sort_depend(test_lists[test_list], 0, 'output/', 'test_data.cam.h0', {})
        for i in sorted_list[test_list].keys():
            assert sorted(cm[i]) == sorted(sorted_list[test_list][i])
