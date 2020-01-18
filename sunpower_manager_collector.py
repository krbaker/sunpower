# coding=utf-8

"""
Collects stats from sunpower management interface

"""
# Diamonds silly rounding to int...
SCALE_FIELDS = ["freq_hz",
                "i_3phsum_a",
                "i_mppt1_a",
                "ltea_3phsum_kwh",
                "p_3phsum_kw",
                "p_mpptsum_kw",
                "stat_ind",
                "t_htsnk_degc",
                "v_mppt1_v",
                "vln_3phavg_v",
                "net_ltea_3phsum_kwh",
                "p_3phsum_kw",
                "q_3phsum_kvar",
                "s_3phsum_kva",
                "dl_cpu_load"]

import sunpower_manager
import diamond.collector
import sys
import urllib2
import json

class SunpowerManagerCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SunpowerManagerCollector, self).get_default_config_help()
        config_help.update({
            'host': "sunpower management system hostname/ip"
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SunpowerManagerCollector, self).get_default_config()
        config.update({
            'host': None
        })
        return config


    def publish_state(self, device, path):
        if device.has_key("STATE"):
            if device["STATE"] == "working":
                self.publish("{}.{}.{}".format(path,device["SERIAL"],"state"), 1)
            elif device["STATE"] == "error":
                self.publish("{}.{}.{}".format(path,device["SERIAL"],"state"), 0)
            else:
                self.publish("{}.{}.{}".format(path,device["SERIAL"],"state"), -1)

    def collect(self):
        host = self.config["host"]
        self.log.error("SunpowerManagerCollector Checking {0}".format(host))
        spm = sunpower_manager.sunpower_manager(host)
        self.log.error("SunpowerManagerCollector Fetching {0}".format(host))
        response = spm.device_list()
        self.log.error("SunpowerManagerCollector Fetched {0}".format(host))
        if response.has_key("devices"):
            for device in response["devices"]:
                self.log.error("SunpowerManagerCollector Pushing {0}".format(device))
                fields = []
                device_type = "unknown"
                if device["DEVICE_TYPE"] == "PVS":
                    device_type = "pvs"
                    fields = ["dl_comm_err",
                              "dl_cpu_load",
                              "dl_err_count",
                              "dl_flash_avail",
                              "dl_mem_used",
                              "dl_scan_time",
                              "dl_skipped_scans",
                              "dl_untransmitted",
                              "dl_uptime"]
                elif device["DEVICE_TYPE"] == "Power Meter":
                    device_type = "meter"
                    fields = ["CAL0",
                              "SWVER",
                              "ct_scl_fctr",
                              "freq_hz",
                              "net_ltea_3phsum_kwh",
                              "p_3phsum_kw",
                              "q_3phsum_kvar",
                              "s_3phsum_kva",
                              "tot_pf_rto"]                
                elif device["DEVICE_TYPE"] == "Inverter":
                    device_type = "inverter"
                    fields = ["freq_hz",
                              "i_3phsum_a",
                              "i_mppt1_a",
                              "ltea_3phsum_kwh",
                              "p_3phsum_kw",
                              "p_mpptsum_kw",
                              "stat_ind",
                              "t_htsnk_degc",
                              "v_mppt1_v",
                              "vln_3phavg_v",
                              "SWVER"]
                for field in fields:
                    if device.has_key(field):
                        if field in SCALE_FIELDS:
                            data = float(device[field]) * 1000
                        else:
                            data = float(device[field])
                        self.log.error("Sunpower {0} {0} {0}".format(field, device["SERIAL"], data))
                        self.publish("{}.{}.{}".format(device_type, device["SERIAL"],field), data)
                    self.publish_state(device, device_type)
        self.log.error("SunpowerManagerCollector Complete {0}".format(host))
