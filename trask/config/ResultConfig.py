#!/usr/bin/python

from .Config import Config
from ..version import __version__

class ResultConfig(Config):
  def __init__(self, location=None, values=None):
    self._restricted = ['refresh']
    super(ResultConfig, self).__init__(location, values)

  def _add_defaults(self):
    self._config['default'] = [{"value": "Completed",
                                "weight": 1}]

  def get(self, command_id):
    self.choose()
    c = 'default'
    if command_id in self.values:
      c = command_id
    return self.values[c]
