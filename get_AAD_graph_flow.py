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

with open("AADflow.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

def search_json(data, target_text, current_path=''):
    results = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{current_path}/{key}" if current_path else key
            if isinstance(value, str) and target_text in value:
                results.append((new_path, value))
            # 递归处理子节点
            results.extend(search_json(value, target_text, new_path))
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = f"{current_path}[{index}]"
            if isinstance(item, str) and target_text in item:
                results.append((new_path, item))
            results.extend(search_json(item, target_text, new_path))
    return results

target_text = "graph.microsoft.com"  # 目标文本
matches = search_json(data, target_text)

if matches:
    print("匹配项及路径：")
    for path, value in matches:
        print(f"路径: {path} -> 值: {value}")
        #teams_webhook_url = "https://aligntech.webhook.office.com/webhookb2/7ed9a6c7-e811-4e71-956c-9e54f8b7d705@9ac44c96-980a-481b-ae23-d8f56b82c605/JenkinsCI/9ecff2f044b44cfcae37b0376ecd1540/9d21b513-f4ee-4b3b-995c-7a422a087a6c/V2-0LzN76qekmVrAPO1b9pX-4MwxVsHKo7lbMnV_iHFb81"
        #message = {
        #"text": f"Message_Test: AAD graph flow is active on ZY psn node."
        #}                                       
        #try:
        #    teams_response = requests.post(
        #    teams_webhook_url,
        #    json=message,
        #    headers={"Content-Type": "application/json"}
        #)
        #    teams_response.raise_for_status()
        #except Exception as e:
        #    print(f"Failed to send alert to MS Teams for {aorchestrator_host}")                    
else:
    print("未找到匹配文本")
    teams_webhook_url = "https://aligntech.webhook.office.com/webhookb2/7ed9a6c7-e811-4e71-956c-9e54f8b7d705@9ac44c96-980a-481b-ae23-d8f56b82c605/JenkinsCI/9ecff2f044b44cfcae37b0376ecd1540/9d21b513-f4ee-4b3b-995c-7a422a087a6c/V2-0LzN76qekmVrAPO1b9pX-4MwxVsHKo7lbMnV_iHFb81"
    message = {
    "text": f"WARNING: AAD graph flow is NOT active on ZY psn node，please check the wireless authentication."
    }
    try:
        teams_response = requests.post(
        teams_webhook_url,
        json=message,
        headers={"Content-Type": "application/json"}
    )
        teams_response.raise_for_status()
    except Exception as e:
        print(f"Failed to send alert to MS Teams for {orchestrator_host}")


