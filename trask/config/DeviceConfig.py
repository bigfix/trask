#!/usr/bin/python

from .Config import Config
from ..version import __version__

class DeviceConfig(Config):
  def __init__(self, location=None, values=None):
    self._restricted = ['device id', 'data source', 'computer name']
    super(DeviceConfig, self).__init__(location, values)

  def _add_defaults(self):
    self._config['operating system'] = [{"value": {"name": "trask", 
                                                   "version": __version__}, 
                                         "weight": 1}]
    self._config['in proxy agent context'] = [{"value": False, 
                                               "weight": 1}]
