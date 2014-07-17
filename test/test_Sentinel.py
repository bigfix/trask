#!/usr/bin/python

import os, sys
import unittest

sys.path.insert(0, os.path.join(
                     os.path.dirname(
                       os.path.dirname(os.path.abspath(__file__))), 'plugin'))
from trask import Sentinel

class TestEqual(unittest.TestCase):
  def test_eq(self):
    a = Sentinel()
    b = Sentinel(a.id, a.name)
    self.assertEqual(a, b)

  def test_not_eq(self):
    a = Sentinel()
    b = Sentinel(a.id+'bolivar', a.name+'moira')
    self.assertNotEqual(a, b)

class TestHash(unittest.TestCase):
  def test_hash(self):
    a = Sentinel()
    self.assertIsNotNone(hash(a))

  def test_eq(self):
    a = Sentinel()
    b = Sentinel(name=a.name)
    self.assertEqual(hash(a), hash(b))

    b.id += 'moira'
    self.assertEqual(hash(a), hash(b))

  def test_not_eq(self):
    a = Sentinel()
    b = Sentinel(a.id, a.name+'moira')
    self.assertNotEqual(hash(a), hash(b))

    a.id += 'bolivar'
    self.assertNotEqual(hash(a), hash(b))

if __name__ == '__main__':
  unittest.main()
