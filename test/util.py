#!/usr/bin/python

import os, tempfile
import json

def write_command(output_directory=None, 
                  command_name=None, 
                  target_device=None, 
                  command_id=None,
                  directory=None):
  command = {}

  if output_directory is not None:
    command['outputDirectory'] = output_directory
  if command_name is not None:
    command['commandName'] = command_name
  if target_device is not None:
    command['targetDevice'] = target_device
  if command_id is not None:
    command['commandID'] = command_id

  cf = tempfile.mkstemp(dir=directory)[1]
  with open(cf, 'w') as f:
    json.dump(command, f, ensure_ascii=False)
  return cf
