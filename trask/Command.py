#!/usr/bin/python

import json

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
