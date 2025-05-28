#!usr/bin/python

import requests
import xml.etree.ElementTree as ET
from requests.auth import HTTPBasicAuth
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def get_response_time(nas_ipaddress):
    url = f"https://10.214.3.102/admin/API/mnt/Session/IPAddress/{nas_ipaddress}"
    headers = {
        "Accept": "application/xml"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            auth=HTTPBasicAuth("ans-api", "P@ssw0rd"),
            verify=False,  # Disable SSL verification for testing purposes
            timeout=30  # Set a timeout for the request
        )
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        return response.text  # Return the output in text format for further processing
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # List of Wireless Controllers and IP addresses
    nas_list = {
        "Chengdu_WLC": "10.133.246.5",
        "ZiYang_WLC": "10.146.230.253",
        "Singapore_WLC": "10.127.230.5",
        "JPtkyo_WLC": "10.121.230.9",
        "INhdrb_WLC": "10.152.230.5"
    }

    for wlc, nas_ipaddress in  nas_list.items():
        print(f"Getting AAD response time for {wlc}")
        response = get_response_time(nas_ipaddress)
        response_time = ET.fromstring(response).findtext("response_time")
        print(f"Response time for {wlc}: {response_time} ms")
        if response_time and int(response_time) > 30000:
            teams_webhook_url = "https://aligntech.webhook.office.com/webhookb2/7ed9a6c7-e811-4e71-956c-9e54f8b7d705@9ac44c96-980a-481b-ae23-d8f56b82c605/JenkinsCI/9ecff2f044b44cfcae37b0376ecd1540/9d21b513-f4ee-4b3b-995c-7a422a087a6c/V2-0LzN76qekmVrAPO1b9pX-4MwxVsHKo7lbMnV_iHFb81"
            message = {
            "text": f"WARNING: AAD Response time for {wlc} is {response_time}ms, which exceeds the threshold of 30000 ms."
            }
            try:
                teams_response = requests.post(
                teams_webhook_url,
                json=message,
                headers={"Content-Type": "application/json"}
            )
                teams_response.raise_for_status()
                print(f"Alert sent to MS Teams for {wlc}.\n")
            except Exception as e:
                print(f"Failed to send alert to MS Teams for {wlc}: {e}")
