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
  sunpower getCMSArticles (-t=<id> | -u=<username> [-p=<password>])
  sunpower getAlerts (-t=<id> | -u=<username> [-p=<password>]) [--dashboard]
  sunpower getSolarEnergyOverTimeAggregateParam (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getSystemInfo [-u=<username>] ([-p=<password>] | [-t=<id>])
  sunpower getSiteInfo (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower UtilityRates (-t=<id> | -u=<username> [-p=<password>]) <zip>
  sunpower utilities (-t=<id> | -u=<username> [-p=<password>])
  sunpower MajorPowerBillUtilities (-t=<id> | -u=<username> [-p=<password>])
  sunpower getBillSavingAmountRest (-t=<id> | -u=<username> [-p=<password>]) 
  sunpower getBillSavingAmount (-t=<id> | -u=<username> [-p=<password>])
  sunpower computeDetailedBillSavings (-t=<id> | -u=<username> [-p=<password>]) 
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

"""
APIs available using this pattern:
https://monitor.us.sunpower.com/CustomerPortal/SystemInfo/SystemInfo.svc/help
"""


class sunpower:
    """A class to access sunpowers api.  This is not a public API so it might fail at any time.
    if you find this usefull please complain to sunpower and your sunpower dealer that they
    do not have a public API"""
    def __init__(self,
                 username = None,
                 password = None,
                 token = None,
                 base = "https://monitor.us.sunpower.com/CustomerPortal/"):
        self.system_info_url = "{0}SystemInfo/SystemInfo.svc/".format(base)
        self.site_info_url = "{0}SiteInfo/SiteInfo.svc/".format(base)
        self.alerts_info_url = "{0}AlertsInfo/AlertsInfo.svc/".format(base)
        self.auth_url = "{0}Auth/Auth.svc/".format(base)
        self.bill_savings_url = "{0}BillSavings/BillSavings.svc/".format(base)
        if not token:
            self.token = self.authenticate(username, password)
        else:
            self.token = token

    def generic_command(self, url, command, id_field, args = {}):
        args.update({id_field: self.token})
        return requests.get(url + command, params = args).json()
        
    def system_info(self, command, id_field = 'id', args = {}):
        print args
        return self.generic_command(self.system_info_url, command, id_field, args)

    def alerts_info(self, command, id_field = 'id', args = {}):
        return self.generic_command(self.alerts_info_url, command, id_field, args)

    def site_info(self, command, id_field = 'id', args = {}):
        return self.generic_command(self.site_info_url, command, id_field, args)

    def bill_savings(self, command, id_field = 'id', args = {}):
        return self.generic_command(self.bill_savings_url, command, id_field, args)

    def get_site_info(self):
        return self.site_info("GetSiteInfo")

    def get_real_time_net_display(self):
        return self.system_info("getRealTimeNetDisplay")

    def get_energy_data(self, interval, start, end):
        """ This appears to take time in local to system time? """
        return self.system_info("getEnergyData", id_field = "guid",
                                args = {"interval": interval,
                                        "startDateTime": self.datetime_to_sunpower(start),
                                        "endDateTime": self.datetime_to_sunpower(end)})

    def get_pv_production_data(self):
        return self.system_info("getPVProductionData")

    def get_pv_consumption_data(self):
        return self.system_info("getPVConsumptionData")

    def get_module_series_info(self):
        return self.system_info("getModuleSeriesInfo")

    def get_ac_pv_module_info(self):
        return self.system_info("getACPVModuleInfo")

    def get_component_tree(self):
        return self.system_info("getComponentTree")

    def get_component_data_last(self, component_type_id, component_id):
        return self.system_info("getComponentDataLast", args = {"componentTypeId": component_type_id,
                                                                "componentId": component_id})

    def get_health_guidance_info(self):
        return self.system_info("getHealthGuidanceInfo")

    def get_system_info(self, username):
        return self.system_info("GetSystemInfo", args = {"username": username})

    def get_latest_timestamp(self):
        return self.site_info("GetLatestTimestamp")

    def get_alerts(self, is_dashboard = True):
        return self.alerts_info("getAlerts", args = {"isDashboard": is_dashboard})

    def get_all_user_preference(self):
        return self.alerts_info("getAllUserPreference")

    def get_cms_articles(self):
        return self.alerts_info("getCMSArticles")

    def utility_rates(self, zip):
        return self.bill_savings("UtilityRates", args = {"postalCode" : zip})

    def major_power_bill_utilities(self):
        return self.bill_savings("MajorPowerBillUtilities")

    def authenticate(self, username, password):
        """Get token from user/password"""
        r = requests.post(self.auth_url + "Authenticate",
                          data = json.dumps({"username": username,
                                             "password": password,
                                             "isPersistent": "false"}),
                          headers = {'Content-type': 'application/json'}
                      )
        return r.json()["Payload"]["TokenID"]

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
    if not arguments["-t"]:
        if not arguments["-u"]:
            print "No Valid Auth"
            sys.exit(1)
        elif not arguments["-p"]:
            arguments["-p"] = getpass.getpass()
        sp = sunpower(username = arguments["-u"], password = arguments["-p"])
        if arguments["authenticate"]:
            print sp.token
            sys.exit(0)
    else:
        sp = sunpower(token = arguments["-t"])
    if arguments["getSiteInfo"]:
        print json_pretty(sp.get_site_info())
    elif arguments["getLatestTimestamp"]:
        print json_pretty(sp.get_latest_timestamp())
    elif arguments["getAlerts"]:
        print json_pretty(sp.get_alerts(arguments["--dashboard"]))
    elif arguments["getAllUserPreference"]:
        print json_pretty(sp.get_all_user_preference())
    elif arguments["getCMSArticles"]:
        print json_pretty(sp.get_cms_articles())
    elif arguments["MajorPowerBillUtilities"]:
        print json_pretty(sp.major_power_bill_utilities())
    elif arguments["UtilityRates"]:
        print json_pretty(sp.utility_rates(arguments["<zip>"]))
    elif arguments["getSystemInfo"]:
        print json_pretty(sp.get_system_info(arguments["-u"]))
    elif arguments["getRealTimeNetDisplay"]:
        print json_pretty(sp.get_real_time_net_display())
    elif arguments["getPVProductionData"]:
        print json_pretty(sp.get_pv_production_data())
    elif arguments["getPVConsumptionData"]:
        print json_pretty(sp.get_pv_consumption_data())
    elif arguments["getModuleSeriesInfo"]:
        print json_pretty(sp.get_module_series_info())
    elif arguments["getHealthGuidanceInfo"]:
        print json_pretty(sp.get_health_guidance_info())
    elif arguments["getACPVModuleInfo"]:
        print json_pretty(sp.get_ac_pv_module_info())
    elif arguments["getComponentTree"]:
        print json_pretty(sp.get_component_tree())
    elif arguments["getComponentDataLast"]:
        print json_pretty(sp.get_component_data_last(arguments["<componentTypeId>"],
                                                     arguments["<componentId>"]))
    elif arguments["getEnergyData"]:
        interval = "minute"
        if arguments["<interval>"]:
            interval = arguments["<interval>"]
        endDateTime = datetime.datetime.now()
        if arguments["<endDateTime>"]:
            endDateTime = arguments["<endDateTime>"]
        startDateTime = (datetime.datetime.now() - datetime.timedelta(hours = 24))
        if arguments["<startDateTime>"]:
            startDateTime = arguments["<startDateTime>"]
        print json_pretty(sp.get_energy_data(interval, startDateTime, endDateTime))
