#!/usr/bin/python

import os, sys, tempfile
import sqlite3
import unittest

sys.path.insert(0, os.path.join(
                     os.path.dirname(
                       os.path.dirname(os.path.abspath(__file__))), 'plugin'))
from trask import MasterMold as MM
from trask import Sentinel

class MasterMold(MM):
  def __init__(self):
    super(MasterMold, self).__init__(tempfile.mkstemp()[1])

class TestDatabase(unittest.TestCase):
  def test_init(self):
    master_mold = MasterMold()
    self.assertIsInstance(master_mold, MasterMold)

  def test_add_get(self):
    master_mold = MasterMold()
    sentinel = Sentinel()
    master_mold.add_sentinel(sentinel)

    sentinels = master_mold.get_sentinels()
    self.assertEqual(len(sentinels), 1)
    self.assertEqual(sentinels[0], sentinel)

  def test_get(self):
    master_mold = MasterMold()
    master_mold.add_sentinel(Sentinel(id='rockets', name='gas'))
    master_mold.add_sentinel(Sentinel(id='stomp', name='palm beam'))
    master_mold.add_sentinel(Sentinel(id='eye beams', name='bomb'))

    self.assertEqual(len(master_mold.get_sentinels(1)), 1)
    self.assertEqual(len(master_mold.get_sentinels(2)), 2)
    self.assertEqual(len(master_mold.get_sentinels(3)), 3)
    self.assertEqual(len(master_mold.get_sentinels()), 3)

  def test_invalid_add(self):
    master_mold = MasterMold()

    a = Sentinel()
    b = Sentinel(a.id, a.name)

    master_mold.add_sentinel(a)
    self.assertRaises(sqlite3.IntegrityError, master_mold.add_sentinel, b)

if __name__ == '__main__':
  unittest.main()
