[![Build Status](https://travis-ci.org/bigfix/trask.svg?branch=master)](https://travis-ci.org/bigfix/trask)

An IBM Endpoint Manager Proxy Agent plugin to simulate clients

# Features
- Generate device reports
  - Computer name
  - Operating system

# Usage
## Prerequisites
- [python-3.x](https://www.python.org/downloads/)

## Environment
- Windows Server
  - IBM Endpoint Manager 9.1.1117.0 - Proxy Agent

## Setup
Tested on `bolivar` a Windows Server 2012 environment:
- IBM Endpoint Manager 9.1.1117.0 - Proxy Agent
- python-3.3.5.amd64

On `bolivar`:

```bash
$ net stop BESProxyAgent
$ cd {Management Extender root folder}
$ mkdir Plugins
$ cd Plugins
$ git clone git@github.com:bigfix/trask.git
$ net start BESProxyAgent
```

`{Management Extender root folder}` by default is `C:\Program Files (x86)\BigFix Enterprise\Management Extender`. Adjust the [`settings.json`](settings.json) if your Proxy Agent was installed elsewhere.

## Configure
### Device reports
Device reports can be configured via the `--device-config` option. To utilize this option, the [`settings.json`](settings.json) must be edited to include the option in the `ExecutablePath`. The `--device-config` option takes a JSON file with the following specifications:
- keys correlate to device report attributes (ex: `operating system`).
- values must be a list of choice objects
.  - choice objects have a mandatory key, `value`, and optional key, `weight`. By default, the `weight` is 1.

For example, this configuration file, [`sentinel.json`](sentinel.json) has two equal likelihood choices for the `operating system` attribute:

```json
{
  "operating system": [{"value": {"name": "bolivar trask", 
                                  "version": "1965.11.10"}, 
                        "weight": 1},
                       {"value": {"name": "moira kinross", 
                                  "version": "1975.12.10"}, 
                        "weight": 1}]
}
```

### Command results
Command results can be configured via the `--result-config` option. Like the configuration for device reports, the [`settings.json`](settings.json) must be edited to include the option in the `ExecutablePath`. This configuration also takes a JSON file with the following specifications:
- keys correlate to commands (ex: `locate`).
- values must be a list of choice objects
.  - choice objects have a mandatory key, `value`, and optional key, `weight`. By default, the `weight` is 1. The value must either be "Completed", "Failed", or "Error".

For example, this configuration file, [`result.json`](result.json) has two equal likelihood choices for the `locate` command and one result for any other commands:

```json
{
  "locate": [{"value": "Completed", 
              "weight": 1},
             {"value": "Failed",
              "weight": 1},
             {"value": "Error",
              "weight": 1}],

  "default": [{"value": "Completed",
               "weight": 1}]
}
```

# Develop
## Prerequisites
- [nose](https://nose.readthedocs.org/en/latest/)
- [vagrant](http://www.vagrantup.com/downloads.html)

## Tests
To run the tests, run any of the following (or execute a test file directly):

```bash
$ python -m unittest discover
```

```bash
$ python test/test_Sentinel.py
```

```bash
$ nosetests
```

Tests can also be built using `vagrant`. To run tests in this way, run the following:

### Linux & Mac
```bash
$ make test
```

### Windows
```bat
> make.bat test
```

# Support
Any issues or questions regarding this software should be filed via [GitHub issues](https://github.com/bigfix/trask/issues).
