#!/usr/bin/python

import os, sys
import json
import random

from argparse import ArgumentParser

class Sentinel:
  def __init__(self, id=None, name=None):
    self.id = hex(random.getrandbits(42*8))[2:]
    self.name = '{0}, {1} {2} sentinel'.format(self.__color(),
                                               self.__adjective(),
                                               self.__generation())

  def __eq__(self, other):
    return (self.id == other.id) or (self.name == other.name)

  def __hash__(self):
    return hash(self.name)

  def __color(self):
    colors = ['aqua', 'black', 'blue', 'fuchsia', 'gray', 'green', 'lime', 
              'maroon', 'navy', 'navy', 'olive', 'orange', 'purple', 'red',
              'silver', 'teal', 'white', 'yellow']
    return colors[random.randint(0,len(colors)-1)]

  def __adjective(self):
    adjectives = ['abandoned', 'able', 'absolute', 'academic', 'acceptable', 
                  'acclaimed', 'accomplished', 'accurate', 'aching', 'acidic', 
                  'acrobatic', 'active', 'actual', 'adept', 'admirable', 
                  'admired', 'adolescent', 'adorable', 'advanced', 
                  'adventurous', 'affectionate', 'afraid']
    return adjectives[random.randint(0,len(adjectives)-1)]

  def __generation(self):
    generations = ['mark ii', 'composite', 'mark iii', 'mark iv', 'mark v', 
                   'mark vi', 'mark vii', 'nimrod', 'prime', 'omega prime',
                   'wild', 'mark viii', 'bio']
    return generations[random.randint(0,len(generations)-1)]

  def is_applicable(self, command):
    if command.exists('targetdevice'):
      return command.get('targetdevice') == self.id
    else:
      return command.get('commandname') == 'refresh'

  def process_command(self, command):
    process = {
      'refresh': {'output': '{0}.report'.format(self.id),
                  'result':  {'device id': self.id,
                              'data source': 'trask',
                              'computer name': self.name}},
      0:         {'output': '{0}.json'.format(command.get('commandid')),
                  'result': {'CommandID': command.get('commandid'),
                             'DeviceID': self.id,
                             'Result': 'Completed'}}
    }

    name = command.get('commandname')
    if command.get('commandname') not in process:
      name = 0

    loc = os.path.join(command.get('outputdirectory'),
                       process[name]['output'])
    with open(loc, 'w') as f:
      json.dump(process[name]['result'], f, ensure_ascii=False)

    if name == 0:
      os.remove(command.location)

class Command:
  def __init__(self, location):
    self.location = location
    with open(location, 'r') as f:
      self.__command = json.load(f, object_hook=Command.__json_lower)
    self.__validate()

  @staticmethod
  def __json_lower(d):
     return dict((k.lower(), d[k]) for k in d)

  def __validate(self):
    is_valid = True

    for k in ['outputdirectory', 'commandname']:
      if not self.exists(k):
        is_valid = False

    if is_valid:
      if self.get('commandname') != 'refresh':
        for k in ['targetdevice', 'commandid']:
          if not self.exists(k):
            return False
      self.requires_result = True
      
  def exists(self, k):
    return k in self.__command

  def get(self, k):
    if self.exists(k):
      return self.__command[k]
    else:
      return ''

class Trask:
  def __init__(self, n):
    self.sentinels = []
    for i in range(n):
      sentinel = Sentinel()
      while sentinel in self.sentinels:
        sentinel = Sentinel()
      self.sentinels.append(sentinel)

  def process_commands(self, location):
    for cf in os.listdir(location):
      command = Command(os.path.join(location, cf))
      if command.requires_result:
        for sentinel in self.sentinels:
          if sentinel.is_applicable(command):
            sentinel.process_command(command)

def parse_args():
  description = """\
An IBM Endpoint Manager Proxy Agent plugin to simulate clients"""

  usage = """Usage: python trask.py [options]

{0}

Options:
  --configOptions OPTIONS  config options
  --commandDir LOCATION    command directory location

  -h, --help               print this help text and exit
  """.format(description)

  argparser = ArgumentParser(description=description,
                             usage=usage,
                             add_help=False)

  argparser.add_argument('--configOptions')
  argparser.add_argument('--commandDir', required=True)

  argparser.add_argument('-h', '--help')

  if '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

  args = argparser.parse_args()

  return args

def main():
  args = parse_args()
  
  trask = Trask(42)
  trask.process_commands(args.commandDir)

if __name__ == '__main__':
  main()
