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
import ipaddress

def main():
  print "Main"
  Subnets=[]

  print "-"*20
  r = requests.get("http://"+sys.argv[1]+"/api/ipam/prefixes/?limit=1000&status=1&cf_DHCP_Enabled=1")
  if r.status_code == 200:
    Prefixes = json.loads(r.text)
    print("{0} Active Prefixes in Netbox").format(Prefixes["count"])

    for Prefix in Prefixes["results"]:
      Subnet = Prefix["prefix"].split("/")
      if Prefix["custom_fields"]["DHCP_Enabled"] is True:
        #print Subnet[0]
        #print ipaddress.IPv4Network(Prefix["prefix"]).netmask
        if Prefix["custom_fields"]["DHCP_StartIP"] is not None and Prefix["custom_fields"]["DHCP_EndIP"] is not None and Prefix["custom_fields"]["DHCP_DNSServer"] is not None and Prefix["custom_fields"]["DHCP_Gateway"] is not None: 
          #print Prefix["custom_fields"]["DHCP - Start IP"]
          #print Prefix["custom_fields"]["DHCP - End IP"] 
          #print Prefix["custom_fields"]["DHCP - DNS Server"]
          SubnetString = Subnet[0]+";"+str(ipaddress.IPv4Network(Prefix["prefix"]).netmask)+";"+Prefix["custom_fields"]["DHCP_StartIP"]+";"+Prefix["custom_fields"]["DHCP_EndIP"]+";"+Prefix["custom_fields"]["DHCP_Gateway"]+";"+Prefix["custom_fields"]["DHCP_DNSServer"]
          Subnets.append(SubnetString)

    #print Subnets
    print("{0} Valid DHCP-Enabled Prefixes in Netbox").format(str(len(Subnets)))
    SubnetsFile = open('subnets.yml', 'wb')
    SubnetsFile.write('dhcp_networks:\n')
    for Subnet in Subnets:
      Subnet = Subnet.split(";")
      #print Subnet
      SubnetsFile.write('  - { subnet: '+Subnet[0]+', netmask: '+Subnet[1]+', StartIP: '+Subnet[2]+', EndIP: '+Subnet[3]+', gateway: '+Subnet[4]+', domain: topgun.cisco.com, dns_server: '+Subnet[5]+' }\n')      

if __name__ == "__main__":
  main()