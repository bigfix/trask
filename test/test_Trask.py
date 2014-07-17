#!/usr/bin/python

import os, sys, tempfile
import unittest

from test.util import write_command

sys.path.insert(0, os.path.join(
                     os.path.dirname(
                       os.path.dirname(os.path.abspath(__file__))), 'plugin'))
from trask import MasterMold as MM
from trask import Trask as T

class MasterMold(MM):
  def __init__(self):
    super(MasterMold, self).__init__(tempfile.mkstemp()[1])

class Trask(T):
  def __init__(self, n):
    super(Trask, self).__init__(n, MasterMold())

class TestRun(unittest.TestCase):
  def test_init(self):
    trask = Trask(0)
    self.assertIsInstance(trask, Trask)

  def test_refresh(self):
    temp = tempfile.mkdtemp()
    dr = os.path.abspath(os.path.join(temp, 'DeviceReports'))
    pr = os.path.abspath(os.path.join(temp, 'PendingRefreshes'))
    os.mkdir(dr)
    os.mkdir(pr)
    cf = write_command(output_directory=dr,
                       command_name='refresh',
                       directory=pr)

    n = 42
    trask = Trask(n)
    trask.process_commands(pr)

    self.assertEqual(len(os.listdir(dr)), n)
    self.assertTrue(os.path.isfile(cf))

if __name__ == '__main__':
  unittest.main()
