# -*- coding: utf-8 -*-
"""
Created on Fri May  8 19:54:59 2020

@author: Reuben
"""

import unittest
import unitty
from unitty import utils
import numpy as np

PD_PRESENT = False
try:
    import pandas as pd
    PD_PRESENT = True
except ImportError:
    print('No pandas')



TEST_DICT_30 = {'base_types': ['length', 'mass', 'time'],
               'length': {'_base': 'm', 
                        'm': [1.0, 'length', 'meter'],
                        'mm': [0.001, 'm', 'millimeter'],
                        'in': [25.4, 'mm', 'inch'],
                        'ft': [12, 'in', 'foot']},
               'mass': {'_base': 'kg', 
                        'kg': [1.0, 'mass', 'kilogram'],
                        'g': [0.001, 'kg', 'gram'],
                        'lbs': [0.45359237, 'kg', 'pound mass']},
               'time': {'_base': 's', 
                        's': [1.0, 'time', 'second']}}


TEST_SYSTEMS_20 = {'metric':
                       {'length': ['mm', 'm'],
                        'mass': ['kg'],
                        'time': ['s']}}

TEST_REF_SET_A = {'widget_length': {'metric': 'mm', 'US': 'in'},
                  'complex.value': {'metric': 'kg.s2/m', 'US': 'lbs.s2/ft'}}

# s = unitty.get_systems('test')
# s.set_refs(TEST_REF_SET_A)

class Test_Units(unittest.TestCase):
    def setUp(self):
        unitty.setup('test', units_raw=TEST_DICT_30, sys_raw=TEST_SYSTEMS_20)
    
    def test_split_str(self):
        s = 'abcd [mm.kg/s]'
        name, units = utils.split_str(s)
        self.assertEqual(name, 'abcd')
        self.assertEqual(units, 'mm.kg/s')
        
    def test_str_to_unit(self):
        s = 'abcd [mm.kg/s]'
        unit = utils.str_to_unit(s)
        self.assertEqual(str(unit), '0.001 kg.m/s')
        
    def test_make_qty(self):
        s = 'abcd [mm.kg/s]'
        q = utils.make_qty(s, 5.7)
        self.assertEqual(str(q), '5.7 kg.mm/s')

    def test_add_unit(self):
        s = 'abcd'
        s2 = utils.add_unit(s, 'kg.mm/s')
        self.assertEqual(s2, 'abcd [kg.mm/s]')
        
    def test_split_qty(self):
        s = 'abcd [m.kg/s]'
        q = utils.make_qty(s, 0.0057)
        s2, val = utils.split_qty(q)
        self.assertEqual(s2, 'abcd [kg.mm/s]')
        self.assertEqual(val, 5.7)
        
    def test_transform_pair(self):
        s = 'abcd [m.kg/s]'
        val = 0.0057
        s2, val2 = utils.transform_pair(s, val)
        self.assertEqual(s2, 'abcd [kg.mm/s]')
        self.assertEqual(val2, 5.7)
        
    def test_transform_dict(self):
        dct = {'abcd [m.kg/s]': 0.0057,
             'efgh [mm2/lbs]': 11.0}
        out = utils.transform_dict(dct)
        v = 11.0*(1/0.45359237)
        expected = {'abcd [kg.mm/s]': 5.7,
                    'efgh [mm2/kg]': v}
        self.assertDictEqual(expected, out)
        
    def test_transform_list_of_dicts(self):
        lst = [{'abcd [m.kg/s]': 0.0057},
                {'efgh [mm2/lbs]': 11.0}]
        out = utils.transform_list_of_dicts(lst)
        v = 11.0*(1/0.45359237)
        expected = [{'abcd [kg.mm/s]': 5.7},
                    {'efgh [mm2/kg]': v}]
        self.assertListEqual(expected, out)

    def test_transform_df(self):
        if not PD_PRESENT:
            return
        lst = [{'abcd [m.kg/s]': 0.0057, 'efgh [mm2/lbs]': 11.0},
                {'abcd [m.kg/s]': 0.009, 'efgh [mm2/lbs]': 17.0}]
        df = pd.DataFrame(lst)
        df2 = utils.transform_df(df)
        v1 = 11.0*(1/0.45359237)
        v2 = 17.0*(1/0.45359237)
        out = df2.to_dict(orient='rows')
        expected = [{'abcd [kg.mm/s]': 5.7, 'efgh [mm2/kg]': v1},
                {'abcd [kg.mm/s]': 9, 'efgh [mm2/kg]': v2}]
        for out_row, expected_row in zip(out, expected):
            for k, v in out_row.items():
                self.assertTrue(k in expected_row)
                self.assertAlmostEqual(v, expected_row[k])
