#!/usr/bin/python

import os, sys
import json
import random
import sqlite3

from version import __version__
from argparse import ArgumentParser

class Config:
  def __init__(self, location=None, values=None):
    self.__config = {}
    self.__add_defaults()

    self.is_valid = False
    self.values = values

    if location is not None:
      with open(location, 'r') as f:
        self.__config = json.load(f)
        self.is_valid = self.__validate()

  def __validate(self):
    for attribute in self.__config:
      if type(self.__config[attribute]) is not list:
        return False

      if attribute in ['device id', 'data source', 'computer name']:
        return False

      for i, choice in enumerate(self.__config[attribute]):
        if type(choice) is not dict:
          return False

        if 'value' not in choice:
          return False

        if 'weight' not in choice:
          self.__config[attribute][i]['weight'] = 1

    return True

  def __add_defaults(self):
    self.__config['operating system'] = [{"value": {"name": "trask", 
                                                   "version": __version__}, 
                                         "weight": 1}]

  def choose(self):
    self.values = {}

    for attribute in self.__config:
      weighted_choices = []
      for i, choice in enumerate(self.__config[attribute]):
        weighted_choices.append((i, choice['weight']))
      choices = [v for v, c in weighted_choices for j in range(c)]
      self.values[attribute] = \
        self.__config[attribute][random.choice(choices)]['value']

class Sentinel:
  def __init__(self, id=None, name=None, config=None):
    if id is None:
      id = hex(random.getrandbits(42*8))[2:]
    if name is None:
      name = '{0}, {1} {2} sentinel'.format(self.__color(),
                                            self.__adjective(),
                                            self.__generation())
    if config is None:
      config = Config()

    self.id = id
    self.name = name
    self.config = config
    if self.config.values is None:
      self.config.choose()

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
                  'adventurous', 'affectionate', 'afraid', 'beautiful']
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

  def _process_refresh(self, command):
    result = {"device id": self.id,
              "data source": "trask",
              "computer name": self.name}
    return dict(self.config.values, **result)

  def _process_command(self, command):
    result = {"CommandID": command.get('commandid'),
              "DeviceID": self.id,
              "Result": "Completed"}
    return result

  def process_command(self, command):
    process = {
      'refresh': {'output': '{0}.report'.format(self.id),
                  'result':  self._process_refresh},
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

    if name == 0:
      os.remove(command.location)

class Command:
  def __init__(self, location):
    self.location = location
    with open(location, 'r') as f:
      self.__command = json.load(f, object_hook=Command.__json_lower)
    self.requires_result = False
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

class MasterMold:
  def __init__(self, db=None):
    if db is None:
      db = 'master_mold.db'

    self._connection = sqlite3.connect(db, isolation_level=None)
    self.cursor = self._connection.cursor()

    self.initialize()

  def initialize(self):
    self.cursor.execute("""\
CREATE TABLE IF NOT EXISTS sentinels
(
  id TEXT NOT NULL,
  name TEXT NOT NULL,
  config_values TEXT NOT NULL,
  PRIMARY KEY ( id, name )
)
""")

  def add_sentinel(self, sentinel):
    config_values = json.dumps(sentinel.config.values, separators=(',', ':'))
    self.cursor.execute('INSERT INTO sentinels (id, name, config_values) '
                        'VALUES (?, ?, ?)',
                        (sentinel.id, sentinel.name, config_values))

  def get_sentinels(self, n=None):
    i = 0
    sentinels = []
    for row in self.cursor.execute('SELECT id, name, config_values '
                                   'FROM sentinels'):
      if (n is not None) and (i == n):
        break

      sentinels.append(Sentinel(row[0], 
                                row[1], 
                                Config(values=json.loads(row[2]))))
      i += 1

    return sentinels

class Trask:
  def __init__(self, n, master_mold=None, config=None):
    if master_mold is None:
      master_mold = MasterMold()

    self.n = n
    self.master_mold = master_mold
    self.config = config

    self.activate()

  def activate(self):
    sentinels = self.master_mold.get_sentinels()

    m = self.n - len(sentinels)
    if m > 0:
      for i in range(m):
        sentinel = Sentinel(config=self.config)
        while sentinel in sentinels:
          sentinel = Sentinel(config=self.config)

        sentinels.append(sentinel)
        self.master_mold.add_sentinel(sentinel)

  def process_commands(self, location):
    for cf in os.listdir(location):
      command = Command(os.path.join(location, cf))
      if command.requires_result:
        for sentinel in self.master_mold.get_sentinels(self.n):
          if sentinel.is_applicable(command):
            sentinel.process_command(command)

def parse_args():
  description = """\
An IBM Endpoint Manager Proxy Agent plugin to simulate clients"""

  usage = """Usage: python trask.py [options]

{0}

Options:
  --configOptions        config options (ignored)
  --commandDir LOCATION  command directory location

  --config LOCATION      sentinel configuration file location
  --validate LOCATION    validates sentinel configuration file and exit

  --version              print program version and exit
  -h, --help             print this help text and exit
  """.format(description)

  argparser = ArgumentParser(description=description,
                             usage=usage,
                             add_help=False)

  argparser.add_argument('--configOptions')
  argparser.add_argument('--commandDir')

  argparser.add_argument('--config')
  argparser.add_argument('--validate')

  argparser.add_argument('-h', '--help')
  argparser.add_argument('--version')

  if '-h' in sys.argv or '--help' in sys.argv:
    print(usage)
    sys.exit()

  if '--version' in sys.argv:
    print(__version__)
    sys.exit()

  args = argparser.parse_args()

  if args.validate:
    valid = 'in'
    if os.path.isfile(args.validate):
      if Config(args.validate).is_valid:
        valid = ''
    print('"{0}" is {1}valid.'.format(args.validate, valid))
    sys.exit()

  if args.commandDir is None:
    print("""\
{0}

trask.py: error: --commandDir is required
""".format(usage))
    sys.exit(1)

  return args

def main():
  args = parse_args()
  
  trask = Trask(42, config=Config(args.config))
  trask.process_commands(args.commandDir)

if __name__ == '__main__':
  main()
