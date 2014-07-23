#!/usr/bin/python

import os, sys
import unittest

from test.util import write_device_config

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trask.config.DeviceConfig import DeviceConfig

class TestWriteConfig(unittest.TestCase):
  def test_write(self):
    cf = write_device_config(operating_system={"name": "bolivar trask",
                                               "version": "1965.11.10"},
                             device_id='14',
                             data_source='jack kirby',
                             computer_name='marvel')
    self.assertTrue(os.path.isfile(cf))

class TestRead(unittest.TestCase):
  def test_valid(self):
    config = DeviceConfig(write_device_config(operating_system=
                                                {"name": "bolivar trask",
                                                 "version": "1965.11.10"}))
    self.assertIsInstance(config, DeviceConfig)
    self.assertTrue(config.is_valid)
    self.assertIsNone(config.values)

  def test_invalid(self):
    config = DeviceConfig(write_device_config(device_id='14'))
    self.assertIsInstance(config, DeviceConfig)
    self.assertFalse(config.is_valid)
    self.assertIsNone(config.values)

    config = DeviceConfig(write_device_config(data_source='jack kirby'))
    self.assertIsInstance(config, DeviceConfig)
    self.assertFalse(config.is_valid)
    self.assertIsNone(config.values)

    config = DeviceConfig(write_device_config(computer_name='marvel'))
    self.assertIsInstance(config, DeviceConfig)
    self.assertFalse(config.is_valid)
    self.assertIsNone(config.values)

  def test_choose(self):
    config = DeviceConfig(write_device_config(operating_system=
                                                {"name": "bolivar trask",
                                                 "version": "1965.11.10"}))
    config.choose()
    self.assertIsNotNone(config.values)

if __name__ == '__main__':
  unittest.main()
