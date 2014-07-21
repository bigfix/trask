#!/usr/bin/python

import json
import random

from .version import __version__

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
    self.__config['in proxy agent context'] = [{"value": False, 
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
