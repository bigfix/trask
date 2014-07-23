#!/usr/bin/python

import os
import json
import random

from .config.DeviceConfig import DeviceConfig
from .config.ResultConfig import ResultConfig
from .Command import Command

class Sentinel:
  def __init__(self, 
               id=None, 
               name=None, 
               device_config=None, 
               result_config=None):
    if id is None:
      id = hex(random.getrandbits(42*8))[2:]
    if name is None:
      name = '{0}, {1} {2} sentinel'.format(self.__color(),
                                            self.__adjective(),
                                            self.__generation())
    if device_config is None:
      device_config = DeviceConfig()
    if result_config is None:
      result_config = ResultConfig()

    self.id = id
    self.name = name
    self.device_config = device_config
    if self.device_config.values is None:
      self.device_config.choose()
    self.result_config = result_config

  def __eq__(self, other):
    return (self.id == other.id) or (self.name == other.name)

  def __hash__(self):
    return hash(self.name)

  def __color(self):
    colors = ['aqua', 'black', 'blue', 'fuchsia', 'gray', 'green', 'lime', 
              'maroon', 'navy', 'navy', 'olive', 'orange', 'purple', 'red',
              'silver', 'teal', 'white', 'yellow']
    return random.choice(colors)

  def __adjective(self):
    adjectives = ['abandoned', 'able', 'absolute', 'academic', 'acceptable', 
                  'acclaimed', 'accomplished', 'accurate', 'aching', 'acidic', 
                  'acrobatic', 'active', 'actual', 'adept', 'admirable', 
                  'admired', 'adolescent', 'adorable', 'advanced', 
                  'adventurous', 'affectionate', 'afraid', 'beautiful']
    return random.choice(adjectives)

  def __generation(self):
    generations = ['mark ii', 'composite', 'mark iii', 'mark iv', 'mark v', 
                   'mark vi', 'mark vii', 'nimrod', 'prime', 'omega prime',
                   'wild', 'mark viii', 'bio']
    return random.choice(generations)

  def is_applicable(self, command):
    if command.exists('targetdevice'):
      return command.get('targetdevice') == self.id
    else:
      return command.get('commandname') == 'refresh'

  def _process_refresh(self, command):
    result = {"device id": self.id,
              "data source": "trask",
              "computer name": self.name}
    return dict(self.device_config.values, **result)

  def _process_command(self, command):
    result = [{"CommandID": command.get('commandid'),
               "DeviceID": self.id,
               "Result": self.result_config.get(command.get('commandname'))}]
    return result

  def process_command(self, command):
    process = {
      'refresh': {'output': '{0}.report'.format(self.id),
                  'result': self._process_refresh},
      0:         {'output': '{0}.json'.format(command.get('commandid')),
                  'result': self._process_command}
    }

    name = command.get('commandname')
    if command.get('commandname') not in process:
      name = 0

    result = os.path.join(command.get('outputdirectory'),
                          process[name]['output'])
    with open(result, 'w') as f:
      json.dump(process[name]['result'](command), f, ensure_ascii=False)

    # if name == 0:
    #   os.remove(command.location)
