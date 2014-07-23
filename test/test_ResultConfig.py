#!/usr/bin/python

import os, sys
import unittest

from test.util import write_result_config

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trask.config.ResultConfig import ResultConfig

class TestWriteConfig(unittest.TestCase):
  def test_write(self):
    cf = write_result_config(locate='Failed',
                             default='Completed')
    self.assertTrue(os.path.isfile(cf))

class TestRead(unittest.TestCase):
  def test_valid(self):
    config = ResultConfig(write_result_config(locate='Failed'))
    self.assertIsInstance(config, ResultConfig)
    self.assertTrue(config.is_valid)
    self.assertIsNone(config.values)

    config = ResultConfig(write_result_config(default='Completed'))
    self.assertIsInstance(config, ResultConfig)
    self.assertTrue(config.is_valid)
    self.assertIsNone(config.values)

    config = ResultConfig(write_result_config(locate='Failed',
                                              default='Completed'))
    self.assertIsInstance(config, ResultConfig)
    self.assertTrue(config.is_valid)
    self.assertIsNone(config.values)

  def test_invalid(self):
    config = ResultConfig(write_result_config(refresh='Failed'))
    self.assertIsInstance(config, ResultConfig)
    self.assertFalse(config.is_valid)
    self.assertIsNone(config.values)

  def test_get(self):
    config = ResultConfig(write_result_config(locate='Failed'))
    self.assertIsNotNone(config.get('locate'))
    self.assertIsNotNone(config.get('default'))

if __name__ == '__main__':
  unittest.main()
