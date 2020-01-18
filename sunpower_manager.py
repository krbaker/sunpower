#!/usr/bin/python
"""
sunpower_manager

Usage:
  sunpower_manager DeviceList <host>
  sunpower_manager -h | --help
  sunpower_manager --version

Options:
  -h --help     Show this screen.
  --version     Show version.
"""

import getpass
import requests
import docopt
import datetime
import sys
import json
from pprint import pprint

from httplib import HTTPConnection
HTTPConnection.debuglevel = 0
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.ERROR)
requests_log.propagate = True


class sunpower_manager:
    """A class to access sunpower management interface 'API'.  This is not a public API so it might fail at any time.
    if you find this usefull please complain to sunpower and your sunpower dealer that they
    do not have a public API"""
    def __init__(self, host = "172.27.153.1"):
        self.command_url = "http://{0}/cgi-bin/dl_cgi?Command=".format(host)

    def generic_command(self, command):
        return requests.get(self.command_url + command).json()
        
    def device_list(self):
        return self.generic_command("DeviceList")


def json_pretty(json_input):
    return json.dumps(json_input, sort_keys=True,
                      indent=4, separators=(',', ': '))

if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version='Sunpower_Manager 1.0')
    spm = sunpower_manager(arguments["<host>"])

    if arguments["DeviceList"]:
        print json_pretty(spm.device_list())
    else:
        print arguments
