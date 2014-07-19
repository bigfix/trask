#!/usr/bin/python

import os, tempfile
import json

def write_command(output_directory=None, 
                  command_name=None, 
                  target_device=None, 
                  command_id=None,
                  directory=None):
  command = {}
  def __write(key, parameter):
    nonlocal command
    if parameter is not None:
      command[key] = parameter

  __write('outputDirectory', output_directory)
  __write('commandName', command_name)
  __write('targetDevice', target_device)
  __write('commandID', command_id)

  cf = tempfile.mkstemp(dir=directory)[1]
  with open(cf, 'w') as f:
    json.dump(command, f, ensure_ascii=False)
  return cf

def write_config(operating_system=None,
                 device_id=None,
                 data_source=None,
                 computer_name=None):
  config = {}
  def __write(key, attribute):
    nonlocal config
    if attribute is not None:
      config[key] = [{"value": attribute,
                      "weight": 1}]

  __write('operating system', operating_system)
  __write('device id', device_id)
  __write('data source', data_source)
  __write('computer name', computer_name)

  cf = tempfile.mkstemp()[1]
  with open(cf, 'w') as f:
    json.dump(config, f, ensure_ascii=False)
  return cf
