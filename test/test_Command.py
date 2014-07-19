#!/usr/bin/python

import os, sys
import unittest

from test.util import write_command

sys.path.insert(0, os.path.join(
                     os.path.dirname(
                       os.path.dirname(os.path.abspath(__file__))), 'plugin'))
from trask import Command

class TestWriteCommand(unittest.TestCase):
  def test_write(self):
    cf = write_command(output_directory='C:\\bolivar')
    self.assertTrue(os.path.isfile(cf))

class TestRead(unittest.TestCase):
  def test_valid(self):
    command = Command(write_command(output_directory='C:\\bolivar',
                                    command_name='refresh'))
    self.assertIsInstance(command, Command)
    self.assertTrue(command.requires_result)

    command = Command(write_command(output_directory='C:\\bolivar',
                                    command_name='capture',
                                    target_device='moira',
                                    command_id='14'))
    self.assertIsInstance(command, Command)
    self.assertTrue(command.requires_result)

  def test_invalid(self):
    command = Command(write_command(output_directory='C:\\bolivar'))
    self.assertIsInstance(command, Command)
    self.assertFalse(command.requires_result)

    command = Command(write_command(command_name='refresh'))
    self.assertIsInstance(command, Command)
    self.assertFalse(command.requires_result)

    command = Command(write_command(command_name='locate'))
    self.assertIsInstance(command, Command)
    self.assertFalse(command.requires_result)

    command = Command(write_command(output_directory='C:\\bolivar',
                                    command_name='capture',
                                    target_device='moira'))
    self.assertIsInstance(command, Command)
    self.assertFalse(command.requires_result)

    command = Command(write_command(output_directory='C:\\bolivar',
                                    command_name='capture',
                                    command_id='14'))
    self.assertIsInstance(command, Command)
    self.assertFalse(command.requires_result)

  def test_exists(self):
    command = Command(write_command(output_directory='C:\\bolivar',
                                    command_name='locate'))
    self.assertTrue(command.exists('outputdirectory'))
    self.assertTrue(command.exists('commandname'))
    self.assertFalse(command.exists('targetdevice'))
    self.assertFalse(command.exists('commandid'))

    command = Command(write_command(output_directory='C:\\bolivar',
                                    command_name='capture',
                                    target_device='moira',
                                    command_id='14'))
    self.assertTrue(command.exists('outputdirectory'))
    self.assertTrue(command.exists('commandname'))
    self.assertTrue(command.exists('targetdevice'))
    self.assertTrue(command.exists('commandid'))

  def test_get(self):
    od = 'C:\\bolivar'
    cn = 'locate'
    command = Command(write_command(output_directory=od,
                                    command_name=cn))
    self.assertEqual(command.get('outputdirectory'), od)
    self.assertEqual(command.get('commandname'), cn)
    self.assertEqual(command.get('targetdevice'), '')
    self.assertEqual(command.get('commandid'), '')

    od = 'C:\\bolivar'
    cn = 'capture'
    td = 'moira'
    ci = '14'
    command = Command(write_command(output_directory=od,
                                    command_name=cn,
                                    target_device=td,
                                    command_id=ci))
    self.assertEqual(command.get('outputdirectory'), od)
    self.assertEqual(command.get('commandname'), cn)
    self.assertEqual(command.get('targetdevice'), td)
    self.assertEqual(command.get('commandid'), ci)

if __name__ == '__main__':
  unittest.main()
