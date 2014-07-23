#!/usr/bin/python

import os, sys, tempfile, subprocess
import unittest

from test.util import write_command

trask_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, trask_path)
from trask.MasterMold import MasterMold as MM
from trask.Trask import Trask as T

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
    result = os.path.abspath(os.path.join(temp, 'DeviceReports'))
    pending = os.path.abspath(os.path.join(temp, 'PendingRefreshes'))
    os.mkdir(result)
    os.mkdir(pending)
    cf = write_command(output_directory=result,
                       command_name='refresh',
                       directory=pending)

    n = 42
    trask = Trask(n)
    trask.process_commands(pending)

    self.assertEqual(len(os.listdir(result)), n)
    self.assertTrue(os.path.isfile(cf))

  def test_locate(self):
    temp = tempfile.mkdtemp()
    result = os.path.abspath(os.path.join(temp, 'ActionResultsFiles'))
    pending = os.path.abspath(os.path.join(temp, 'PendingCommands'))
    os.mkdir(result)
    os.mkdir(pending)
    n = 42
    trask = Trask(n)

    cfs = []
    sentinels = trask.master_mold.get_sentinels()
    for i, sentinel in enumerate(sentinels):
      cfs.append(write_command(output_directory=result,
                               command_name='locate',
                               target_device=sentinel.id,
                               command_id='3141592653-{0}'.format(i),
                               directory=pending))

    trask.process_commands(pending)
    self.assertEqual(len(os.listdir(result)), n)

    for cf in cfs:
      self.assertFalse(os.path.isfile(cf))

class TestModule(unittest.TestCase):
  def __run(self, args):
    try:
      subprocess.check_call(args, cwd=trask_path, stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
      self.fail('Failed with return code ({0})'.format(e.returncode))

  def test_import(self):
    self.__run([sys.executable, '-c', 'from trask.Command import *'])
    self.__run([sys.executable, '-c', 'from trask.config.Config import *'])
    self.__run([sys.executable, '-c', 
                'from trask.config.DeviceConfig import *'])
    self.__run([sys.executable, '-c', 
                'from trask.config.ResultConfig import *'])
    self.__run([sys.executable, '-c', 'from trask.MasterMold import *'])
    self.__run([sys.executable, '-c', 'from trask.Sentinel import *'])
    self.__run([sys.executable, '-c', 'from trask.Trask import *'])
    self.__run([sys.executable, '-c', 'from trask.version import *'])

class TestExecution(unittest.TestCase):
  def __run(self, args):
    try:
      subprocess.check_call(args, cwd=os.path.join(trask_path, 'plugin'), 
                            stdout=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
      self.fail('Failed with return code ({0})'.format(e.returncode))

  def test_version(self):
    self.__run([sys.executable, '-m', 'trask', '--version'])

  def test_help(self):
    self.__run([sys.executable, '-m', 'trask', '--help'])
    self.__run([sys.executable, '-m', 'trask', '-h'])

if __name__ == '__main__':
  unittest.main()
