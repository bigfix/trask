#!/usr/bin/python

import os, sys
import json
import random
import unittest

sys.path.insert(0, os.path.join(
                     os.path.dirname(
                       os.path.dirname(os.path.abspath(__file__))), 'plugin'))
from trask import Command

def write_command(output_directory=None, 
                  command_name=None, 
                  target_device=None, 
                  command_id=None):
  command = {}

  if output_directory is not None:
    command['outputDirectory'] = output_directory
  if command_name is not None:
    command['commandName'] = command_name
  if target_device is not None:
    command['targetDevice'] = target_device
  if command_id is not None:
    command['commandID'] = command_id

  cf = '{0}.command'.format(hex(random.getrandbits(42*8))[2:])
  while os.path.isfile(cf):
    cf = '{0}.command'.format(hex(random.getrandbits(42*8))[2:])

  with open(cf, 'w') as f:
    json.dump(command, f, ensure_ascii=False)
  return cf

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
    command = Command(write_command(output_directory='C:\\bolivar',
                                    command_name='locate'))
    self.assertEqual(command.get('outputdirectory'), 'C:\\bolivar')
    self.assertEqual(command.get('commandname'), 'locate')
    self.assertEqual(command.get('targetdevice'), '')
    self.assertEqual(command.get('commandid'), '')

    command = Command(write_command(output_directory='C:\\bolivar',
                                    command_name='capture',
                                    target_device='moira',
                                    command_id='14'))
    self.assertEqual(command.get('outputdirectory'), 'C:\\bolivar')
    self.assertEqual(command.get('commandname'), 'capture')
    self.assertEqual(command.get('targetdevice'), 'moira')
    self.assertEqual(command.get('commandid'), '14')

if __name__ == '__main__':
  unittest.main()
