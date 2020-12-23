#!/usr/bin/python
"""
sunpower

Usage:
  sunpower get_user (-u=<username> [-p=<password>])
  sunpower get_address (-u=<username> [-p=<password>])
  sunpower get_activity (-u=<username> [-p=<password>])
  sunpower get_alerts (-u=<username> [-p=<password>])
  sunpower get_components (-u=<username> [-p=<password>])
  sunpower get_power (-u=<username> [-p=<password>])
  sunpower authenticate -u=<username> [-p=<password>]
  sunpower -h | --help
  sunpower --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -t Auth Token
  -u username
  -p password
  --dashboard
"""

#Commands were found here: https://monitor.us.sunpower.com/CustomerPortal/SystemInfo/SystemInfo.svc/help

import getpass
import requests
import docopt
import datetime
import sys
import json
from pprint import pprint

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.ERROR)
requests_log.propagate = True

"""
APIs taken from watching the webapi interactions
with some pointers from https://github.com/jeffkowalski/sunpower
"""


class sunpower:
    """A class to access sunpowers api.  This is not a public API so it might fail at any time.
    if you find this usefull please complain to sunpower and your sunpower dealer that they
    do not have a public API"""
    def __init__(self,
                 username = None,
                 password = None,
                 base = "https://elhapi.edp.sunpower.com/v{}/elh/{}"):
        self.base = base
        self.authenticate(username, password)
            
    def generic_command(self, api_version, command):
        r = requests.get(self.base.format(api_version, command),
                         headers = {"Authorization": "SP-CUSTOM {}".format(self.token)})
        r.raise_for_status()
        return r.json()
        
    def get_user(self):
        return self.generic_command("1","user/{}".format(self.user))

    def get_address(self):
        return self.generic_command("1","address/{}/".format(self.address))

    def get_activity(self):
        return self.generic_command("1","address/{}/activity?async=false".format(self.address))

    def get_alerts(self):
        return self.generic_command("1","address/{}/alerts?async=false".format(self.address))

    def get_components(self):
        return self.generic_command("1","address/{}/components?async=false".format(self.address))

    def get_power(self):
        return self.generic_command("1","address/{}/power?async=false".format(self.address))
    
    def authenticate(self, username, password):
        """Get token from user/password"""
        r = requests.post(self.base.format("1","authenticate"),
                          data = json.dumps({"username": username,
                                             "password": password,
                                             "isPersistent": "false"}),
                          headers = {'Content-type': 'application/json'}
                      )
        j = r.json()
        self.token = j["tokenID"]
        self.address = j["addressId"]
        self.addresses = j["addresses"]
        self.user = j["userId"]
        self.account = j["accountId"]


    def datetime_to_sunpower(self, in_datetime):
        in_datetime = in_datetime.replace(microsecond = 0)
        in_datetime = in_datetime.replace(second = 0)
        return in_datetime.isoformat("T")



def json_pretty(json_input):
    return json.dumps(json_input, sort_keys=True,
                      indent=4, separators=(',', ': '))

if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version='Sunpower 1.0')
    sp = None
    if not arguments["-u"]:
        print ("No Valid Auth")
        sys.exit(1)
    elif not arguments["-p"]:
        arguments["-p"] = getpass.getpass()
    sp = sunpower(username = arguments["-u"], password = arguments["-p"])
    if arguments["authenticate"]:
        print (sp.token)
        sys.exit(0)
    if arguments["get_user"]:
        print (json_pretty(sp.get_user()))
    elif arguments["get_address"]:
        print (json_pretty(sp.get_address()))
    elif arguments["get_activity"]:
        print (json_pretty(sp.get_activity()))
    elif arguments["get_alerts"]:
        print (json_pretty(sp.get_alerts()))
    elif arguments["get_components"]:
        print (json_pretty(sp.get_components()))
    elif arguments["get_power"]:
        print (json_pretty(sp.get_power()))

