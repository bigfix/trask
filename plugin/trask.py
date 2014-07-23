#!/usr/bin/python

import os, sys

from argparse import ArgumentParser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trask.config.DeviceConfig import DeviceConfig
from trask.config.ResultConfig import ResultConfig
from trask.Trask import Trask
from trask.version import __version__

def parse_args():
  description = """\
An IBM Endpoint Manager Proxy Agent plugin to simulate clients"""

  usage = """Usage: python trask.py [options]

{0}

Options:
  --configOptions           config options (ignored)
  --commandDir LOCATION     command directory location

  --device-config LOCATION  sentinel configuration file location
  --result-config LOCATION  command result configuration file location
  --validate                validates configuration file and exit
                            (must specify "--device-config" or "result-config")

  --version                 print program version and exit
  -h, --help                print this help text and exit
  """.format(description)

  def error_with_usage(message):
    nonlocal usage
    print("""\
{0}

trask.py: error: {1}
""".format(usage, message))
    sys.exit(1)

  argparser = ArgumentParser(description=description,
                             usage=usage,
                             add_help=False)

  argparser.add_argument('--configOptions')
  argparser.add_argument('--commandDir')

  argparser.add_argument('--device-config')
  argparser.add_argument('--result-config')
  argparser.add_argument('--validate', action='store_true')

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
    if (args.device_config and args.result_config) or \
       not args.device_config or \
       not args.result_config:
      error_with_usage('must specify "--device-config" or "result-config"')

    valid = 'in'
    config = None
    if args.device_config:
      config = args.device_config
      if os.path.isfile(config) and DeviceConfig(config).is_valid:
          valid = ''

    if args.result_config:
      config = args.result_config
      if os.path.isfile(config) and ResultConfig(config).is_valid:
          valid = ''

    print('"{0}" is {1}valid.'.format(config, valid))
    sys.exit()

  if args.commandDir is None:
    error_with_usage('--commandDir is required')

  return args

def main():
  args = parse_args()
  
  trask = Trask(42, 
                device_config=DeviceConfig(args.device_config), 
                result_config=ResultConfig(args.result_config))
  trask.process_commands(args.commandDir)

if __name__ == '__main__':
  main()
