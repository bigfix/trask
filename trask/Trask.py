#!/usr/bin/python

import os

from .MasterMold import MasterMold
from .Sentinel import Sentinel
from .config.DeviceConfig import DeviceConfig
from .Command import Command

class Trask:
  def __init__(self, n, master_mold=None, device_config=None):
    if master_mold is None:
      master_mold = MasterMold()

    self.n = n
    self.master_mold = master_mold
    self.device_config = device_config

    self.activate()

  def activate(self):
    sentinels = self.master_mold.get_sentinels()

    m = self.n - len(sentinels)
    if m > 0:
      for i in range(m):
        sentinel = Sentinel(device_config=self.device_config)
        while sentinel in sentinels:
          sentinel = Sentinel(device_config=self.device_config)

        sentinels.append(sentinel)
        self.master_mold.add_sentinel(sentinel)

  def process_commands(self, location):
    for cf in os.listdir(location):
      command = Command(os.path.join(location, cf))
      if command.requires_result:
        for sentinel in self.master_mold.get_sentinels(self.n):
          if sentinel.is_applicable(command):
            sentinel.process_command(command)
