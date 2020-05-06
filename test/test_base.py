# -*- coding: utf-8 -*-
"""
Created on Tue May  5 09:46:59 2020

@author: Reuben
"""

import unittest
from unitty import base
import numpy as np

TEST_DICT_1 = {'base_types': ['length'],
               'length': {'_base': 'm', 
                        'm': [1.0, 'length', 'meter']}}

TEST_DICT_2 = {'base_types': ['length'],
               'length': {'_base': 'm', 
                        'm': [1.0, 'length', 'meter'],
                        'mm': [0.001, 'm', 'millimeter']}}

TEST_DICT_3 = {'base_types': ['length', 'area'],
               'length': {'_base': 'm', 
                        'm': [1.0, 'length', 'meter']},
               'area': {'_base': 'm2', 
                        'm2': [1.0, ['m', 'm'], 'square meter']}}
    
TEST_DICT_4 = {'base_types': ['length', 'mass', 'time', 'force'],
               'length': {'_base': 'm', 
                        'm': [1.0, 'length', 'meter'],
                        'mm': [0.001, 'm', 'millimeter']},
               'mass': {'_base': 'kg', 
                        'kg': [1.0, 'mass', 'kilogram']},
               'time': {'_base': 's', 
                        's': [1.0, 'time', 'second']},
               'force': {'_base': 'N', 
                        'N': [1.0, ['kg', 'm', '-s', '-s'], 'newton']}}

TEST_DICT_5 = {'base_types': ['length', 'mass'],
               'length': {'_base': 'm', 
                        'm': [1.0, 'length', 'meter'],
                        'cm': [0.01, 'm', 'centimeter'],
                        'in': [2.54, 'cm', 'inch'],
                        'ft': [12, 'in', 'foot']},
               'mass': {'_base': 'kg', 
                        'kg': [1.0, 'mass', 'kilogram'],
                        'lbs': [0.45359237, 'kg', 'pound mass']},
               }

TEST_DICT_6 = {'base_types': ['length', 'mass'],
               'length': {'_base': 'm', 
                        'm': [1.0, 'length', 'meter', {'SI_prefixes': ['c']}],
                        'in': [2.54, 'cm', 'inch'],
                        'ft': [12, 'in', 'foot']},
               'mass': {'_base': 'kg', 
                        'kg': [1.0, 'mass', 'kilogram'],
                        'lbs': [0.45359237, 'kg', 'pound mass']},
               }


class Test_Units(unittest.TestCase):
    
    def test_load_1(self):
        b = base.Units(raw=TEST_DICT_1)
        self.assertEqual(len(b.units), (1+1)*2)
        expected = {1: 'length',
                    -1: '-length',
                    2: 'm',
                    -2: '-m'}
        self.assertDictEqual(b._num_dct, expected)
        expected = {'length': 1,
                    '-length': -1,
                    'm': 2,
                    '-m': -2}
        self.assertDictEqual(b._ind_dct, expected)
        self.assertDictEqual(b.bases, {1: 2})
        self.assertDictEqual(b._utypes, {-2: -1, -1: -1, 1: 1, 2: 1})
        
    def test_load_2(self):
        b = base.Units(raw=TEST_DICT_2)
        self.assertEqual(len(b.units), (1+2)*2)
        expected = {1: 'length',
                    -1: '-length',
                    2: 'm',
                    -2: '-m',
                    3: 'mm',
                    -3: '-mm'}
        self.assertDictEqual(b._num_dct, expected)
        expected = {'length': 1,
                    '-length': -1,
                    'm': 2,
                    '-m': -2,
                    'mm': 3,
                    '-mm': -3}
        self.assertDictEqual(b._ind_dct, expected)
        self.assertDictEqual(b.bases, {1: 2})
        self.assertDictEqual(b._utypes, {-3: -1, -2: -1, -1: -1, 1: 1, 2: 1,
                                         3: 1})

    def test_load_3(self):
        b = base.Units(raw=TEST_DICT_3)
        self.assertEqual(len(b.units), (2+2)*2)
        expected = {1: 'length',
                    -1: '-length',
                    2: 'area',
                    -2: '-area',
                    3: 'm',
                    -3: '-m',
                    4: 'm2',
                    -4: '-m2'}
        self.assertDictEqual(b._num_dct, expected)
        expected = {'length': 1,
                    '-length': -1,
                    'area': 2,
                    '-area': -2,
                    'm': 3,
                    '-m': -3,
                    'm2': 4,
                    '-m2': -4}
        self.assertDictEqual(b._ind_dct, expected)
        self.assertDictEqual(b.bases, {1: 3, 2: 4})
        self.assertDictEqual(b._utypes, {-4: -2, -3: -1, -2: -2, -1: -1, 1: 1,
                                         2: 2, 3: 1, 4: 2})
    
    def test_getattr_mm(self):
        b = base.Units(raw=TEST_DICT_2)
        u = b.mm
        self.assertEqual(u.value, 0.001)
        self.assertEqual(u.abbr, 'mm')

    def test_spec_mm(self):
        b = base.Units(raw=TEST_DICT_2)
        u = b.mm
        self.assertEqual(u.value, 0.001)        
        mm_ind = b._ind('mm')
        self.assertSequenceEqual(u.spec, [mm_ind])
        
    def test_getitem_mm(self):
        b = base.Units(raw=TEST_DICT_2)
        u = b['mm']
        self.assertEqual(u.value, 0.001)
        self.assertEqual(u.abbr, 'mm')
        
    def test_get_by_index(self):
        b = base.Units(raw=TEST_DICT_2)
        ret = b.get_by_index(2)
        self.assertEqual(ret, b.m)
        ret = b.get_by_index(-3)
        self.assertEqual(ret, b['-mm'])
        
    def test_str_spec(self):
        b = base.Units(raw=TEST_DICT_4)
        N_p_mm = b.N / b.mm
        ind_N = b.N.spec[0]
        ind_mm = b.mm.spec[0]
        self.assertEqual(N_p_mm.value, 1000.0)
        self.assertEqual(N_p_mm.abbr, None)
        self.assertEqual(N_p_mm.spec, [ind_N, -ind_mm])
        s = b.str_spec(N_p_mm.spec)
        self.assertEqual(s, 'N/mm')
        
    def test_derive(self):
        b = base.Units(raw=TEST_DICT_4)
        spec = ['N', '-mm']
        val, vec = b._derive(spec)
        self.assertEqual(val, 1000.0)
        self.assertTrue(np.allclose(vec, [0, 1, -2, 0]))

    def test_spec_from_str_1(self):
        b = base.Units(raw=TEST_DICT_4)
        s = 'kg'
        spec = b.spec_from_str(s)
        check = b.str_spec(spec)
        self.assertEqual(s, check)
        
    def test_spec_from_str_2(self):
        b = base.Units(raw=TEST_DICT_4)
        s = 'N/kg'
        spec = b.spec_from_str(s)
        check = b.str_spec(spec)
        self.assertEqual(s, check)
        
    def test_spec_from_str_3(self):
        b = base.Units(raw=TEST_DICT_4)
        s = '1/kg'
        spec = b.spec_from_str(s)
        check = b.str_spec(spec)
        self.assertEqual(s, check)
        
    def test_spec_from_str_4(self):
        b = base.Units(raw=TEST_DICT_4)
        s = 's/(kg.m)'
        spec = b.spec_from_str(s)
        check = b.str_spec(spec)
        self.assertEqual(s, check)
        
    def test_spec_from_str_5(self):
        b = base.Units(raw=TEST_DICT_4)
        s = 's2'
        spec = b.spec_from_str(s)
        check = b.str_spec(spec)
        self.assertEqual(s, check)
        
    def test_from_str(self):
        b = base.Units(raw=TEST_DICT_4)
        n_current = len(b.units)
        s = 'm/s2'
        unit = b.from_str(s)
        self.assertEqual(unit.abbr, 'm/s2')
        self.assertTrue(unit.abbr, b.units)
        self.assertEqual(len(b.units), n_current + 2)
        
