# coding=utf-8

"""
Collects stats from sunpower

"""

import diamond.collector
import sys
import urllib2
import json
import sunpower

class SunpowerCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SunpowerCollector, self).get_default_config_help()
        config_help.update({
            'username': "username to sunpower site",
            'password': "password to sunpower site"
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SunpowerCollector, self).get_default_config()
        config.update({
            'username': None,
            'password': None
        })
        return config

    def collect(self):
        sp = sunpower.sunpower(username = self.config['username'],
                               password = self.config['password'])
        response = sp.get_ac_pv_module_info()
        if response.has_key("Payload") and response["Payload"].has_key("ACPVModulePosition"):
            for module in response["Payload"]["ACPVModulePosition"]:
                self.publish("panel.{}".format(module["SerialNumber"]), module["currentGeneration"] * 1000)

