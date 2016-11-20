#!/usr/bin/python
"""
sunpower

Usage:
  sunpower getACPVModuleInfo (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getComponentDataLast (-t=<id> | -u=<username> [-p=<password>]) <componentTypeId> <componentId>
  sunpower getComponentTree (-t=<id> | -u=<username> [-p=<password>])  
  sunpower getEnergyData (-t=<id> | -u=<username> [-p=<password>]) [<interval>] [<startDateTime>] [<endDateTime>]
  sunpower getEnergyDataDownload (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getEnergyDataNoCache (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getEnvironmentImpact (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getHealthGuidanceInfo (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getHourlyEnergyData (-t=<id> | -u=<username> [-p=<password>]) [<timestamp>]
  sunpower getComponentTree (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getModuleSeriesInfo (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getPVConsumptionData (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getPVProductionData (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getRealTimeNetDisplay (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getSolarEnergyOverTime (-t=<id> | -u=<username> [-p=<password>])
  sunpower getUserPreference (-t=<id> | -u=<username> [-p=<password>]) <key>
  sunpower getAllUserPreference (-t=<id> | -u=<username> [-p=<password>])
  sunpower getAlerts (-t=<id> | -u=<username> [-p=<password>]) [--dashboard]
  sunpower getSolarEnergyOverTimeAggregateParam (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getSystemInfo [-u=<username>] ([-p=<password>] | [-t=<id>])
  sunpower getSiteInfo (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getLatestTimestamp (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower linkRainforest (-t=<id> | -u=<username> [-p=<password>]) <cloud_id>
  sunpower unlinkRainforest (-t=<id> | -u=<username> [-p=<password>]) <cloud_id>
  sunpower validateSerial (-t=<id> | -u=<username> [-p=<password>]) <serial>
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

from httplib import HTTPConnection
HTTPConnection.debuglevel = 0
import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.ERROR)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.ERROR)
requests_log.propagate = True

BASE_URL = "https://monitor.us.sunpower.com/CustomerPortal/SystemInfo/SystemInfo.svc/"
AUTH_URL = "https://monitor.us.sunpower.com/CustomerPortal/Auth/Auth.svc/"
SITE_URL = "https://monitor.us.sunpower.com/CustomerPortal/SiteInfo/SiteInfo.svc/"
ALERT_URL = "https://monitor.us.sunpower.com/CustomerPortal/AlertsInfo/AlertsInfo.svc/"

actions = {}
def action(func):
    actions[func.__name__] = func
    return func

@action
def getUserPreference(args):
    url = ALERT_URL + "getUserPreference" + "?id=" + args["-t"] + "&key=" + args["<key>"]
    r = requests.get(url)
    pprint(r.json())

@action
def getAlerts(args):
    url = ALERT_URL + "getAlerts" + "?id=" + args["-t"] + "&isDashboard="
    if args["--dashboard"]:
        url += "true"
    else:
        url += "false"
    r = requests.get(url)
    pprint(r.json())

@action
def getAllUserPreference(args):
    url = ALERT_URL + "getAllUserPreference" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getACPVModuleInfo(args):
    """Gets a lot of system data back including per-panel production!"""
    url = BASE_URL + "getACPVModuleInfo" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getSiteInfo(args):
    """Gets a lot of system data back including per-panel production!"""
    url = SITE_URL + "getSiteInfo" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getLatestTimestamp(args):
    """Gets a lot of system data back including per-panel production!"""
    url = SITE_URL + "GetLatestTimestamp" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def authenticate(args):
    """Get token from user/password"""
    url = AUTH_URL + "Authenticate"
    r = requests.post(url,
                      data = json.dumps({"username": args["-u"],
                                         "password": args["-p"],
                                         "isPersistent": "false"}),
                      headers = {'Content-type': 'application/json'}
                      )
    token = r.json()["Payload"]["TokenID"]
    return token

@action
def getComponentTree(args):
    """Gets a tree of devices, seems like monitoring hardware and inverters in my case"""
    url = BASE_URL + "getComponentTree" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getComponentDataLast(args):
    """ This seems to be able to fetch extra data about a part of the system, haven't found where to get type ids but 1 seems to be a panel
    I get data back using the moduleId from getACPVModuleInfo but its less data than there"""
    url = BASE_URL + "getComponentDataLast" + "?id=" + args["-t"] + "&componentTypeId=" + args["<componentTypeId>"] + "&componentId=" + args["<componentId>"]
    r = requests.get(url)
    pprint(r.json())

@action
def getHealthGuidanceInfo(args):
    """ Small bit of system health info """
    url = BASE_URL + "getHealthGuidanceInfo" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getSystemInfo(args):
    """ Small bit of system health info """
    url = BASE_URL + "getSystemInfo" + "?id=" + args["-t"]
    if args["-u"]:
        url += "&username=" + args["-u"]
    r = requests.get(url)
    pprint(r.json())

@action
def getRealTimeNetDisplay(args):
    """ Small bit of system health info """
    url = BASE_URL + "getRealTimeNetDisplay" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getPVProductionData(args):
    """ Small bit of system health info """
    url = BASE_URL + "getPVProductionData" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getPVConsumptionData(args):
    """ Small bit of system health info """
    url = BASE_URL + "getPVConsumptionData" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getModuleSeriesInfo(args):
    """ Small bit of system health info """
    url = BASE_URL + "getModuleSeriesInfo" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getEnvironmentImpact(args):
    """ Small bit of system health info """
    url = BASE_URL + "getEnvironmentImpact" + "?id=" + args["-t"]
    r = requests.get(url)
    pprint(r.json())

@action
def getEnergyData(args):
    """ Get overall system power history, looks like this is in system local time 'minute' returns every five minutes for me """
    if args["<startDateTime>"] == None:
        start = (datetime.datetime.now() - datetime.timedelta( hours = 24))
        start = start.replace(microsecond = 0)
        args["<startDateTime>"] = start.isoformat("T")
    if args["<endDateTime>"] == None:
        end = datetime.datetime.now()
        end = end.replace(microsecond = 0)
        args["<endDateTime>"] = end.isoformat("T")
    if args["<interval>"] == None:
        args["<interval>"] = "minute"
    url = BASE_URL + "getEnergyData" + "?guid=" + args["-t"] + "&startDateTime=" + args["<startDateTime>"] + "&endDateTime=" + args["<endDateTime>"] + "&interval=" + args["<interval>"]
    print url
    r = requests.get(url)
    pprint(r.json())

@action
def getHourlyEnergyData(args):
    """ Get hourly energy data defaults to a day"""
    if args["<timestamp>"] == None:
        start = (datetime.datetime.now())
        start = start.replace(microsecond = 0)
        start = start.replace(second = 0)
        start = start.replace(minute = 0)
        start = start - datetime.timedelta(hours = 24)
        args["<timestamp>"] = start.isoformat("T")
    url = BASE_URL + "getHourlyEnergyData" + "?tokenid=" + args["-t"] + "&timestamp=" + args["<timestamp>"]
    r = requests.get(url)
    pprint(r.json())

if __name__ == "__main__":
    arguments = docopt.docopt(__doc__, version='Sunpower 1.0')
    if not arguments["-t"]:
        if not arguments["-u"]:
            print "No Valid Auth"
            sys.exit(1)
        elif not arguments["-p"]:
            arguments["-p"] = getpass.getpass()
        arguments["-t"] = authenticate(arguments)
        if arguments["authenticate"]:
            print arguments["-t"]
            sys.exit(0)
    for a in actions:
        if arguments.has_key(a) and arguments[a] == True:
            actions[a](arguments)
