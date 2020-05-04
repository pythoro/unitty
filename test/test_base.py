# -*- coding: utf-8 -*-
"""
Created on Tue May  5 09:46:59 2020

@author: Reuben
"""

import unittest
from unitty import base

class Test_Units(unittest.TestCase):
    def test_getattr_mm(self):
        u = base.units.mm
        self.assertEqual(u.value, 0.001)
        self.assertEqual(u.abbr, 'mm')

    def test_spec(self):
        u = base.units.mm
        self.assertEqual(u.value, 0.001)        
        mm_ind = base.units._ind('mm')
        self.assertSequenceEqual(u.spec, [mm_ind])
        
    def test_getitem_mm(self):
        u = base.units['mm']
        self.assertEqual(u.value, 0.001)
        self.assertEqual(u.abbr, 'mm')