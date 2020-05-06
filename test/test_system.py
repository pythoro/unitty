# -*- coding: utf-8 -*-
"""
Created on Wed May  6 10:29:40 2020

@author: Reuben
"""

import unittest
import unitty
import numpy as np
import os

from .test_base import TEST_DICT_5

root = os.path.dirname(os.path.abspath(__file__))

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

TEST_DICT_10 = {'base_types': ['length', 'mass', 'time'],
               'length': {'_base': 'm', 
                        'm': [1.0, 'length', 'meter'],
                        'mm': [1e-3, 'm', 'millimeter'],
                        'ft': [12*0.0254, 'm', 'foot']},
               'mass': {'_base': 'kg', 
                        'kg': [1.0, 'mass', 'kilogram'],
                        'lbs': [0.45359237, 'kg', 'pound mass']},
               'time': {'_base': 's', 
                        's': [1.0, 'time', 'second']}}

TEST_QID_SET_A = {'widget_length': {'metric': 'mm', 'US': 'in'},
                  'complex.value': {'metric': 'kg.s2/m', 'US': 'lbs.s2/ft'}}


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

    def test_quantity_in_sys(self):
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_1)
        u = unitty.get_units('test')
        q = 7 << u.ft / u.lbs
        val, spec = q.in_sys()
        self.assertAlmostEqual(val, 4.703782825976547)
        self.assertEqual(spec, 'm/kg')
        
    def test_quantity_in_sys_switch(self):
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_1)
        u = unitty.get_units('test')
        q = 7 << u.ft / u.lbs
        unitty.set_system('US')
        val, spec = q.in_sys()
        self.assertEqual(val, 7)
        self.assertEqual(spec, 'ft/lbs')
    
    def _round_trip(self, name):
        u = unitty.get_units(name)
        q = 2 << u.m / u.kg
        val, spec = q.in_sys()
        expected = 2
        self.assertAlmostEqual(expected, val)
        unitty.set_system('US')
        val, spec = q.in_sys()
        self.assertAlmostEqual(2.0, q.value)
        expected = 2 * (1/(12*0.0254)) / (1/0.45359237) # 2.976327887139108
        self.assertAlmostEqual(expected, val)
        q2 = val << u.ft / u.lbs
        val2, spec2 = q2.in_sys()
        self.assertAlmostEqual(2.0, q2.value)
        expected2 = 2 * (1/(12*0.0254)) / (1/0.45359237) # 2.976327887139108
        self.assertAlmostEqual(expected2, val2)
        unitty.set_system('metric')
        val3, spec3 = q2.in_sys()
        self.assertAlmostEqual(2.0, val3)
        
    
    def test_quantity_unitise_round_trip(self):
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_1)
        self._round_trip('test')
        
    def test_quantity_unitise_round_trip_2(self):
        ''' Check for alternative specification '''
        unitty.setup('test', units_raw=TEST_DICT_5, sys_raw=TEST_SYSTEMS_2)
        self._round_trip('test')
        
    def test_set_qids(self):
        unitty.setup('test', units_raw=TEST_DICT_10, sys_raw=TEST_SYSTEMS_1)
        s = unitty.get_systems('test')
        s.set_qids(TEST_QID_SET_A)
        self.assertDictEqual(TEST_QID_SET_A, s._qids)

    def test_set_qids_csv(self):
        unitty.setup('test', units_raw=TEST_DICT_10, sys_raw=TEST_SYSTEMS_1)
        s = unitty.get_systems('test')
        source = os.path.join(root, 'qid_set_1.csv')
        s.set_qids(source)
        self.assertEqual(s._qids['widget_length']['metric'], 'mm')
        self.assertEqual(s._qids['widget_length']['US'], 'in')
        self.assertEqual(s._qids['complex.value']['metric'], 'kg.s2/m')
        self.assertEqual(s._qids['complex.value']['US'], 'lbs.s2/ft')
        
    def test_quantity_by_qid(self):
        unitty.setup('test', units_raw=TEST_DICT_10, sys_raw=TEST_SYSTEMS_1)
        s = unitty.get_systems('test')
        source = os.path.join(root, 'qid_set_1.csv')
        s.set_qids(source)
        u = unitty.get_units('test')
        q = 7 << u['kg.s2/m']
        q.set_qid('complex.value')
        val, spec = q.by_qid()
        self.assertEqual(val, 7)
        self.assertEqual(spec, 'kg.s2/m')
        
    def test_quantity_by_qid_switch(self):
        unitty.setup('test', units_raw=TEST_DICT_10, sys_raw=TEST_SYSTEMS_1)
        s = unitty.get_systems('test')
        source = os.path.join(root, 'qid_set_1.csv')
        s.set_qids(source)
        u = unitty.get_units('test')
        q = 7 << u['kg.s2/m']
        q.set_qid('complex.value')
        unitty.set_system('US')
        val, spec = q.by_qid()
        self.assertEqual(val, 7 / (0.45359237 / (12*0.0254)))
        self.assertEqual(spec, 'lbs.s2/ft')