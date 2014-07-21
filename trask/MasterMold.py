#!/usr/bin/python

import json
import sqlite3

from .Sentinel import Sentinel
from .Config import Config

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
