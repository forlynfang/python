#!usr/bin/python3

"""
This script is to check the AAD graph flow on the specific Silver Peak appliance.
Jenkins will run the job and send message to MS Teams for the graph flow down.
Set the Orchestrator and Token in environment
export ORCHESTRATOR_HOST="your.orchestrator.host"
export ORCH_TOKEN="your_secret_token_here"
"""

import json
import requests
from urllib3.exceptions import InsecureRequestWarning
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

orchestrator_host = "aligntech-orch-use1.silverpeak.cloud"
auth_token = "d40fd7fe734f409c9e6bd9532e79a29b089c6a33d66141199cc6e92ba6ff711f8b08bf824bb04410abda5b2724e4ac18090e08b373d04e5eaf7c0c1871b4fef5"

url = "https://aligntech-orch-use1.silverpeak.cloud/gms/rest/flow?nePk=141.NE&ip1=10.146.30.48&mask1=32&port2=443&ipEitherFlag=false&portEitherFlag=false&protocol=tcp&dscp=any&filter=all&edgeHA=false&builtIn=false&uptime=anytime&bytes=total&duration=any&maxFlows=10000"
headers = {
        "Accept": "application/json",
        "X-Auth-Token": auth_token,
    }    
try:
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        response.raise_for_status()
        data = response.json()
        # print(f"ZY_PSN_Flow：{response.json()}") 
except Exception as e:
        print(f"Error: {e}")    

flows = data['flows']
for flow in flows:
 if "graph.microsoft.com" in flow:
    print(f"WARNING: AAD graph flow is active on ZY psn node.")
 #else:
    #print(f"WARNING: AAD graph flow is active on ZY psn node.")



