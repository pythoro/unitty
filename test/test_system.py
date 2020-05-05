# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:29:40 2020

@author: Reuben
"""

import unittest
import unitty
import numpy as np

from .test_base import TEST_DICT_5

TEST_SYSTEMS_1 = {'metric':
                       {'length': ['m'],
                        'mass': ['kg']},
                  'US':
                       {'length': ['ft'],
                        'mass': ['lbs']}}

TEST_SYSTEMS_2 = {'metric':
                       {'length': ['m'],
                        'mass': ['kg']},
                  'US':
                       {'length': ['in', [3, 'ft']],
                        'mass': ['lbs']}}

class Test_Systems(unittest.TestCase):
    
    def test_val(self):
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_1)
        u = unitty.get_units('test')
        q = 7 * u.ft / u.lbs
        self.assertAlmostEqual(q, 7 * (12*0.0254) / 0.45359237)

    def test_quantity_val(self):
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_1)
        u = unitty.get_units('test')
        q = 7 << u.ft / u.lbs
        self.assertAlmostEqual(q.value, 7 * (12*0.0254) / 0.45359237) # 4.703782825976547

    def test_quantity_unitise(self):
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_1)
        u = unitty.get_units('test')
        q = 7 << u.ft / u.lbs
        val, spec = q._unitise()
        self.assertAlmostEqual(val, 4.703782825976547)
        self.assertListEqual(spec, [3, -7])
        
    def test_quantity_unitise_switch(self):
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_1)
        u = unitty.get_units('test')
        q = 7 << u.ft / u.lbs
        unitty.set_system('US')
        val, spec = q._unitise()
        self.assertEqual(val, 7)
        self.assertListEqual(spec, [6, -8])
    
    def _round_trip(self, name):
        u = unitty.get_units(name)
        q = 2 << u.m / u.kg
        val, spec = q._unitise()
        expected = 2
        self.assertAlmostEqual(expected, val)
        unitty.set_system('US')
        val, spec = q._unitise()
        self.assertAlmostEqual(2.0, q.value)
        expected = 2 * (1/(12*0.0254)) / (1/0.45359237) # 2.976327887139108
        self.assertAlmostEqual(expected, val)
        q2 = val << u.ft / u.lbs
        val2, spec2 = q2._unitise()
        self.assertAlmostEqual(2.0, q2.value)
        expected2 = 2 * (1/(12*0.0254)) / (1/0.45359237) # 2.976327887139108
        self.assertAlmostEqual(expected2, val2)
        unitty.set_system('metric')
        val3, spec3 = q2._unitise()
        self.assertAlmostEqual(2.0, val3)
        
    
    def test_quantity_unitise_round_trip(self):
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_1)
        self._round_trip('test')
        
    def test_quantity_unitise_round_trip_2(self):
        ''' Check for alternative specification '''
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_2)
        self._round_trip('test')