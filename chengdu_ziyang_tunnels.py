#!usr/bin/python3

import os
import requests
import json
from dotenv import load_dotenv
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Load environment variables from .env file
load_dotenv(dotenv_path=".env")
orchestrator_host = os.getenv("ORCHESTRATOR_HOST")
auth_token = os.getenv("ORCH_TOKEN")

#TODO: Function to get the list of tunnels from targeted appliances
def get_tunnel_list(source, dest_list):
    url = f"https://{orchestrator_host}/gms/rest/tunnels2/physical?nePk={source}&limit=500"
    headers = {
        "Accept": "application/json",
        "X-Auth-Token": auth_token,
    }
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        response.raise_for_status()
        tunnels = response.json()
#        print(json.dumps(tunnels, indent=2))
        tunnel_list = []
        for tunnel_id, tunnel_info in tunnels.items():
            if tunnel_info.get("destNePk") in dest_list:
                tunnel_name = tunnel_info.get("alias")
                tunnel_list.append(tunnel_name)

    except Exception as e:
        print(f"Error: {e}")

    return tunnel_list

#TODO: Function to get the DOWN tnnels and compare to targeted list
def get_tunnels_down(appliance_name, appliance_id, tunnel_list):
    url = f"https://{orchestrator_host}/gms/rest/tunnels2/physical?nePk={appliance_id}&limit=100&state=Down"
    headers = {
        "Accept": "application/json",
        "X-Auth-Token": auth_token,
    }
    try:
        response = requests.get(url, headers=headers, verify=False, timeout=30)
        response.raise_for_status()
        tunnels = response.json()

        for tunnel_id, tunnel_info in tunnels.items():
            tunnel_name = tunnel_info.get("alias")

            if tunnel_name in tunnel_list:
                with open("baseline_tunnels.txt", "r") as f:
                    baseline = json.load(f)
                    if tunnel_name in baseline:
                        print(f"INFO: On {appliance_name}, the tunnel {tunnel_name} is in previous list of DOWN tunnels.")
                    else:
                        print(f"WARNING: On {appliance_name}, the tunnel {tunnel_name} is DOWN.")
                        teams_webhook_url = "https://aligntech.webhook.office.com/webhookb2/7ed9a6c7-e811-4e71-956c-9e54f8b7d705@9ac44c96-980a-481b-ae23-d8f56b82c605/JenkinsCI/9ecff2f044b44cfcae37b0376ecd1540/9d21b513-f4ee-4b3b-995c-7a422a087a6c/V2-0LzN76qekmVrAPO1b9pX-4MwxVsHKo7lbMnV_iHFb81"
                        message = {
                        "text": f"WARNING: On {appliance_name}, the tunnel {tunnel_name} is DOWN."
                        }
                        try:
                            teams_response = requests.post(
                            teams_webhook_url,
                            json=message,
                            headers={"Content-Type": "application/json"}
                        )
                            teams_response.raise_for_status()
                        except Exception as e:
                            print(f"Failed to send alert to MS Teams for {appliance_name}")
                        
                        baseline.append(tunnel_name)
                        with open("baseline_tunnels.txt", "w") as fh:
                            json.dump(baseline, fh, indent=2)
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Generate the list of destination appliances to get the tunnel list, and check the tunnels down are in the list or not
    # The list of destination appliances to check tunnels
    """
    Mapping Appliance name and ID
    AWS-APN1-ECV-1 --> 82.NE
    AWS-APN1-ECV-2 --> 83.NE
    AWS-CNN1-ECV-1 --> 101.NE
    AWS-CNN1-ECV-2 --> 102.NE
    AWS-USW2-ECV-1 --> 90.NE
    AWS-USW2-ECV-2 --> 91.NE
    Azure-West-US2-ECV-1 --> 95.NE 
    Azure-West-US2-ECV-2 --> 96.NE
    GCP-USW4-ECV-1 --> 156.NE
    GCP-USW4-ECV-2 --> 157.NE
    usscla01sp01 --> 12.NE
    usscla01sp02 --> 13.NE
    sgsing01sp01 --> 43.NE
    sgsing01sp02 --> 44.NE
    mxjuar02sp01 --> 41.NE
    mxjuar02sp02 --> 42.NE
    iltela02sp01 --> 158.NE
    iltela02sp02 --> 159.NE
    """
    chengdu_dest_list = ["82.NE", "83.NE", "101.NE", "102.NE", "90.NE", "91.NE", "95.NE", "96.NE", "156.NE", "157.NE", "12.NE", "13.NE", "43.NE", "44.NE"]
    chengdu_tunnel_list = get_tunnel_list("145.NE", chengdu_dest_list)
    # Display the tunnel list for debugging
    #print(chengdu_tunnel_list)

    # Check the tunnels on Chengdu Treat SP01, ID "145.NE"
    get_tunnels_down("cnchen02sp01", "145.NE", chengdu_tunnel_list)

    # Check the tunnels on Chengdu Treat SP02, ID "146.NE"
    get_tunnels_down("cnchen02sp02", "146.NE", chengdu_tunnel_list)

    ziyang_dest_list = ["82.NE", "83.NE", "101.NE", "102.NE", "90.NE", "91.NE", "95.NE", "96.NE", "156.NE", "157.NE", "12.NE", "13.NE", "43.NE", "44.NE", "41.NE", "42.NE", "158.NE", "159.NE"]
    ziyang_tunnel_list = get_tunnel_list("141.NE", ziyang_dest_list)
    # Display the tunnel list for debugging
    #print(ziyang_tunnel_list)

    # Check the tunnels on Ziyang Treat SP01, ID "141.NE"
    get_tunnels_down("cnzyng02sp01", "141.NE", ziyang_tunnel_list)

    # Check the tunnels on Ziyang Treat SP02, ID "142.NE"
    get_tunnels_down("cnzyng02sp02", "142.NE", ziyang_tunnel_list)