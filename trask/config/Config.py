#!/usr/bin/python

import json
import random

class Config:
  def __init__(self, location=None, values=None):
    self._config = {}
    self._add_defaults()

    self.is_valid = False
    self.values = values

    if self._restricted is None:
      self._restricted = []

    if location is not None:
      with open(location, 'r') as f:
        self._config = json.load(f)
        self.is_valid = self.__validate()

  def __validate(self):
    for parameter in self._config:
      if type(self._config[parameter]) is not list:
        return False

      if parameter in self._restricted:
        return False

      for i, choice in enumerate(self._config[parameter]):
        if type(choice) is not dict:
          return False

        if 'value' not in choice:
          return False

        if 'weight' not in choice:
          self._config[parameter][i]['weight'] = 1

    return True

  def choose(self):
    self.values = {}

    for parameter in self._config:
      weighted_choices = []
      for i, choice in enumerate(self._config[parameter]):
        weighted_choices.append((i, choice['weight']))
      choices = [v for v, c in weighted_choices for j in range(c)]
      self.values[parameter] = \
        self._config[parameter][random.choice(choices)]['value']
