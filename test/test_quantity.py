# -*- coding: utf-8 -*-
"""
Created on Tue May  5 10:12:00 2020

@author: Reuben
"""

import numpy as np
import unittest
from unitty.quantity import Quantity

class Test_Quantity(unittest.TestCase):
    def setUp(self):
        vector = np.zeros(8, dtype=np.uint8)
        vector[1] = 1.0
        self.vector = vector
    
    def test_init(self):
        q = Quantity(value=1.0, spec=[3, -7], vector=self.vector,
                     abbr='m', name='meter')
        self.assertEqual(q.value, 1.0)
        self.assertSequenceEqual(q.spec, [3, -7])
        self.assertTrue(np.allclose(self.vector, q.vector))
        self.assertEqual(q.abbr, 'm')
        self.assertEqual(q.name, 'meter')
        
    def test_set_unit_valid(self):
        q = Quantity(value=1.0, spec=[3], vector=self.vector,
                     abbr='m', name='meter')
        q2 = Quantity(value=0.001, spec=[8], vector=self.vector,
                     abbr='mm', name='millimeter')
        q.set_unit(q2)
        self.assertEqual(q.value, 0.001)
        self.assertSequenceEqual(q.spec, [8])
        self.assertTrue(np.allclose(self.vector, q.vector))
        self.assertEqual(q.abbr, 'mm')
        self.assertEqual(q.name, 'millimeter')
        
    def test_set_unit_invalid(self):
        q = Quantity(value=1.0, spec=[3], vector=self.vector,
                     abbr='m', name='meter')
        v2 = self.vector.copy()
        v2[4] = 1
        q2 = Quantity(value=0.001, spec=[8], vector=v2,
                     abbr='other', name='other')
        with self.assertRaises(ValueError):
            q.set_unit(q2)

    def test_quantity_multiply(self):
        q1 = Quantity(value=0.001, spec=[3], vector=self.vector,
                     abbr='mm', name='millimeter')
        q = q1 * q1
        self.assertEqual(q.value, 0.000001)
        self.assertSequenceEqual(q.spec, [3, 3])
        self.assertTrue(np.allclose(self.vector*2, q.vector))
        self.assertEqual(q.abbr, None)
        self.assertEqual(q.name, None)
        
    def test_scalar_rmultiply(self):
        q1 = Quantity(value=0.001, spec=[3], vector=self.vector,
                     abbr='mm', name='millimeter')
        q = 5 * q1
        self.assertEqual(q, 0.001*5)

    def test_scalar_multiply(self):
        q1 = Quantity(value=0.001, spec=[3], vector=self.vector,
                     abbr='mm', name='millimeter')
        q = q1 * 5
        self.assertEqual(q, 0.001*5)
        
    def test_quantity_divide(self):
        q1 = Quantity(value=1, spec=[1], vector=self.vector,
                     abbr='m', name='meter')
        q2 = Quantity(value=0.001, spec=[3], vector=self.vector,
                     abbr='mm', name='millimeter')
        q = q1 / q2
        self.assertEqual(q.value, 1000.0)
        self.assertSequenceEqual(q.spec, [1, -3])
        self.assertTrue(np.allclose(self.vector*0, q.vector))
        self.assertEqual(q.abbr, None)
        self.assertEqual(q.name, None)
        
    def test_scalar_rdivide(self):
        q1 = Quantity(value=0.001, spec=[3], vector=self.vector,
                     abbr='mm', name='millimeter')
        q = 5 / q1
        self.assertEqual(q, 5/0.001)

    def test_scalar_divide(self):
        q1 = Quantity(value=0.001, spec=[3], vector=self.vector,
                     abbr='mm', name='millimeter')
        q = q1 / 5
        self.assertEqual(q, 0.001/5)
    
    def test_scalar_lshift(self):
        q1 = Quantity(value=0.001, spec=[3], vector=self.vector,
                     abbr='mm', name='millimeter')
        q = 5 << q1
        self.assertEqual(q.value, 0.005)
        self.assertSequenceEqual(q.spec, [3])
        self.assertTrue(np.allclose(self.vector, q.vector))
        self.assertEqual(q.abbr, None)
        self.assertEqual(q.name, None)

    def test_scalar_rshift(self):
        q1 = Quantity(value=0.001, spec=[3], vector=self.vector,
                     abbr='mm', name='millimeter')
        q = 5 >> q1
        self.assertEqual(q, 5000)
        
    def test_non_unity_div(self):
        vector = np.zeros(8, dtype=np.uint8)
        vector[2] = 1.0
        q1 = Quantity(value=1.7, spec=[1], vector=vector,
                     abbr='s', name='meter')
        q2 = Quantity(value=0.0254*12, spec=[3], vector=self.vector,
                     abbr='ft', name='ft')
        q = q1 / q2
        self.assertEqual(q.value, (1.7)/(0.0254*12)) # 5.57742782152231
        
    def test_non_unity_div(self):
        vector = np.zeros(8, dtype=np.uint8)
        vector[2] = 1.0
        q1 = Quantity(value=1.7, spec=[1], vector=vector,
                     abbr='s', name='meter')
        q2 = Quantity(value=0.0254*12, spec=[3], vector=self.vector,
                     abbr='ft', name='ft')
        q = q1 * q2
        self.assertEqual(q.value, (1.7)*(0.0254*12)) # 0.51816

