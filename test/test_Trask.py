#!/usr/bin/python

import os, sys, tempfile, subprocess
import unittest

from test.util import write_command

trask_path = os.path.join(
                     os.path.dirname(
                       os.path.dirname(os.path.abspath(__file__))), 'plugin')
sys.path.insert(0, trask_path)
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

class TestExecution(unittest.TestCase):
  def __run(self, args):
    try:
      subprocess.check_call(args, cwd=trask_path, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
      self.fail('Failed with return code ({0})'.format(e.returncode))

  def test_import(self):
    self.__run([sys.executable, '-c', 'import trask'])

  def test_version(self):
    self.__run([sys.executable, '-m', 'trask', '--version'])

  def test_help(self):
    self.__run([sys.executable, '-m', 'trask', '--help'])
    self.__run([sys.executable, '-m', 'trask', '-h'])

if __name__ == '__main__':
  unittest.main()
