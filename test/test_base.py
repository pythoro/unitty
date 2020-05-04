# -*- coding: utf-8 -*-
"""
Created on Tue May  5 09:46:59 2020

@author: Reuben
"""

import unittest
from unitty import base

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

    def test_spec(self):
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