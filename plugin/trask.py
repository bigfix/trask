#!/usr/bin/python

import os, sys
import json
import random
import sqlite3

from argparse import ArgumentParser

class Sentinel:
  def __init__(self, id=None, name=None):
    if id is None:
      id = hex(random.getrandbits(42*8))[2:]
    if name is None:
      name = '{0}, {1} {2} sentinel'.format(self.__color(),
                                            self.__adjective(),
                                            self.__generation())

    self.id = id
    self.name = name

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

class MasterMold:
  def __init__(self):
    db = 'master_mold.db'
    initialize = False
    if not os.path.isfile(db):
      initialize = True

    self._connection = sqlite3.connect(db, isolation_level=None)
    self.cursor = self._connection.cursor()

    if initialize:
      self.initialize()

  def initialize(self):
    self.cursor.execute("""\
CREATE TABLE sentinels
(
  id TEXT NOT NULL,
  name TEXT NOT NULL,
  PRIMARY KEY ( id, name )
)
""")

  def add_sentinel(self, sentinel):
    self.cursor.execute('INSERT INTO sentinels (id, name) '
                        'VALUES (?, ?)',
                        (sentinel.id, sentinel.name))

  def get_sentinels(self, n=None):
    i = 0
    sentinels = []
    for row in self.cursor.execute('SELECT id, name from sentinels'):
      if (n is not None) and (i == n):
        break

      sentinels.append(Sentinel(row[0], row[1]))
      i += 1

    return sentinels

class Trask:
  def __init__(self, n):
    self.n = n
    self.master_mold = MasterMold()
    sentinels = self.master_mold.get_sentinels()

    m = n - len(sentinels)
    if m > 0:
      for i in range(m):
        sentinel = Sentinel()
        while sentinel in sentinels:
          sentinel = Sentinel()

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
