#!usr/bin/python3

"""
This script is to check the tunnels down on the specific Silver Peak appliance.
Jenkins will run the job and send message to MS Teams for the tunnels down.
Set the Orchestrator and Token in environment
export ORCHESTRATOR_HOST="your.orchestrator.host"
export ORCH_TOKEN="your_secret_token_here"
"""

import json
import requests
from urllib3.exceptions import InsecureRequestWarning
from dotenv import load_dotenv
import os

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

load_dotenv(dotenv_path=".env")
orchestrator_host = os.getenv("ORCHESTRATOR_HOST")
auth_token = os.getenv("ORCH_TOKEN")

# Handling the missing of host and token
if not orchestrator_host or not auth_token:
    raise EnvironmentError("Missing ORCHESTRATOR_HOST or ORCH_TOKEN environment variable.")

def get_appliance_info(orchestrator_host):
    url = f"https://{orchestrator_host}/gms/rest/appliance"
    headers = {
        "Accept": "application/json",
        "X-Auth-Token": auth_token,
    }
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        response.raise_for_status()
        appliance_list = response.json()
    except Exception as e:
        print(f"Error: {e}")

#    print(appliance_list)
    appliance_info = []
    for appliance in appliance_list:
        appliance_id = appliance.get("id")
        appliance_name = appliance.get("hostName")
        appliance_info.append({appliance_name: appliance_id})

        with open("appliance_info.json", "w") as f:
            json.dump(appliance_info, f, indent=2)

    return appliance_info

def get_tunnels_down(orchestrator_host, appliance_info):
    for appliance in appliance_info:
        for appliance_name, appliance_id in appliance.items():
                url = f"https://{orchestrator_host}/gms/rest/tunnels2/physical?nePk={appliance_id}&limit=20&state=Down"
                headers = {
                    "Accept": "application/json",
                    "X-Auth-Token": auth_token,
                }
                if appliance_id == "145.NE":
                    try:
                        response = requests.get(url, headers=headers, verify=False, timeout=30)
                        response.raise_for_status()
                        tunnels = response.json()
                        print(tunnels)

                        #for tunnel_id, tunnel_info in tunnels.items():
                            #dest_tunnel = tunnel_info.get("alias")
                            #status = tunnel_info.get("operStatus")
                            
                            # Sending the alerts to MS Teams
                            #teams_webhook_url = "https://aligntech.webhook.office.com/webhookb2/7ed9a6c7-e811-4e71-956c-9e54f8b7d705@9ac44c96-980a-481b-ae23-d8f56b82c605/JenkinsCI/9ecff2f044b44cfcae37b0376ecd1540/9d21b513-f4ee-4b3b-995c-7a422a087a6c/V2-0LzN76qekmVrAPO1b9pX-4MwxVsHKo7lbMnV_iHFb81"
                            #message = {
                            #"text": f"WARNING: On {appliance_name}, the tunnel {dest_tunnel} is {status}."
                            #}
                            #try:
                                #teams_response = requests.post(
                                #teams_webhook_url,
                                #json=message,
                                #headers={"Content-Type": "application/json"}
                            #)
                                #teams_response.raise_for_status()
                            #except Exception as e:
                                #print(f"Failed to send alert to MS Teams for {appliance_name}")

                    except Exception as e:
                        print(f"Error: {e}")

if __name__ == "__main__":
    appliance_info = get_appliance_info(orchestrator_host)
    pune_down_tunnels = get_tunnels_down(orchestrator_host, appliance_info)

