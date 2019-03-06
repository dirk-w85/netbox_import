#!/usr/bin/env python
# -*- coding: UTF-8 -*-# enable debugging
print """
Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

             https://developer.cisco.com/docs/licenses
               
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""
__author__ = "Dirk Woellhaf <dwoellha@cisco.com>"
__contributors__ = [
    "Dirk Woellhaf <dwoellha@cisco.com>"
]
__copyright__ = "Copyright (c) 2019 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"


import json
import requests
import ConfigParser
import sys

def main():
  print "Main"
  ZabbixHosts={}

  print "-"*20
  r = requests.get("http://"+sys.argv[1]+"/api/ipam/ip-addresses/?limit=1000")
  if r.status_code == 200:
    IpAddresses = json.loads(r.text)
    print("{0} Ip-Addresses in Netbox").format(IpAddresses["count"])

    for Ip in IpAddresses["results"]:
      Address = Ip["address"].split("/")
      if len(Ip["tags"]) >= 1:
        for Tag in Ip["tags"]:
          if "Zabbix" in Tag and Ip["description"] != "":
            if Tag not in ZabbixHosts:
              ZabbixHosts[Tag] = []
              ZabbixHosts[Tag].append(Address[0]+","+Ip["description"])
            else:
              ZabbixHosts[Tag].append(Address[0]+","+Ip["description"])

    ZabbixFile = open('zabbix_hosts.yml', 'wb')
    for Template in ZabbixHosts:
      ZabbixFile.write(Template+':\n')
      for Host in ZabbixHosts[Template]:
        Host = Host.split(",")
        ZabbixFile.write('  - { ip: '+Host[0]+', name: "'+Host[1].lower()+'" }\n')      

if __name__ == "__main__":
  main()