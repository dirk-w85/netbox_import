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
  PrometheusTargets=[]
  PrometheusNode={}
  PrometheusPing={}

  print "-"*20
  r = requests.get("http://"+sys.argv[1]+"/api/ipam/ip-addresses/?limit=1000&status=1")
  if r.status_code == 200:
    IpAddresses = json.loads(r.text)
    print("{0} Active Ip-Addresses in Netbox").format(IpAddresses["count"])

    for Ip in IpAddresses["results"]:
      if Ip["status"]["label"] == "Active":
        if " " in Ip["description"]:
            Ip["description"] = Ip["description"].replace(" ", "_")

        if len(Ip["tags"]) >= 1:
          for Tag in Ip["tags"]:
            if "Prometheus-Node_Exporter" in Tag and Ip["description"] != "":
              if Ip["tenant"]["name"] not in PrometheusNode:
                PrometheusNode[Ip["tenant"]["name"]] = []
                PrometheusNode[Ip["tenant"]["name"]].append(Ip["description"])
              else:
                PrometheusNode[Ip["tenant"]["name"]].append(Ip["description"])
           
            if "Prometheus-Ping" in Tag and Ip["description"] != "":
              if Ip["tenant"] != None:
                if Ip["tenant"]["name"] not in PrometheusPing:
                  PrometheusPing[Ip["tenant"]["name"]] = []
                  PrometheusPing[Ip["tenant"]["name"]].append(Ip["description"])
                else:
                  PrometheusPing[Ip["tenant"]["name"]].append(Ip["description"])                
          
    
    #print PrometheusNode

    PrometheusTargets = "["
    for Tenant in PrometheusNode:    
      PrometheusTargets += '\n { \n  "labels": { "env": "internal", "tenant": "'+Tenant+'" },\n  "targets": ['
      for Node in PrometheusNode[Tenant]:
        PrometheusTargets += '"'+Node.lower()+':9100",'

      if (PrometheusTargets[-1] == ','):
        PrometheusTargets = PrometheusTargets[:-1]

      PrometheusTargets += '] \n },'

    if (PrometheusTargets[-1] == ','):
      PrometheusTargets = PrometheusTargets[:-1]
    PrometheusTargets += "\n]"

    #print PrometheusTargets
      

    PrometheusNodeFile = open('node_targets.json', 'wb')
    PrometheusNodeFile.write(PrometheusTargets)

    PrometheusTargets = "["
    for Tenant in PrometheusPing:    
      PrometheusTargets += '\n { \n  "labels": { "env": "internal", "tenant": "'+Tenant+'" },\n  "targets": ['
      for Node in PrometheusPing[Tenant]:
        PrometheusTargets += '"'+Node.lower()+'",'

      if (PrometheusTargets[-1] == ','):
        PrometheusTargets = PrometheusTargets[:-1]

      PrometheusTargets += '] \n },'

    if (PrometheusTargets[-1] == ','):
      PrometheusTargets = PrometheusTargets[:-1]
    PrometheusTargets += "\n]"

    #print PrometheusTargets
      

    PrometheusBlackBoxFile = open('blackbox_targets.json', 'wb')
    PrometheusBlackBoxFile.write(PrometheusTargets)
     


if __name__ == "__main__":
  main()