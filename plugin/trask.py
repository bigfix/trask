#!/usr/bin/python

import os, sys

from argparse import ArgumentParser

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trask.Config import Config
from trask.Trask import Trask
from trask.version import __version__

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
