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
from colorama import init, Fore, Style
init(autoreset=True) 
from netmiko import ConnectHandler
os.chdir('C:/Users/ffang/Downloads')
current_dir = os.getcwd()
print(f"当前工作目录：{current_dir}")

# 定义设备连接参数
cisco_device = {
    'device_type': 'cisco_ios',  # 设备类型固定值
    'host': '10.133.20.119',
    'username': 'ffang-admin',
    'password': 'Kaidelakebm@2025',
    'port': 22,  # 默认SSH端口
}

# 建立连接并执行命令
try:
    with ConnectHandler(**cisco_device) as conn:
        text = conn.send_command('sho logging | in alert')  # 执行单条命令
        #print(text)
                
        # 执行多条配置命令
        #config_commands = ['interface GigabitEthernet0/1', 'description Python-configured']
        #output = conn.send_config_set(config_commands)
        #print(output)
        
except Exception as e:
    print(f"连接失败: {str(e)}")

target = "alert"


# 覆盖写入模式（文件存在则清空后保存）
with open("output.txt", "w", encoding="utf-8") as f:  # 推荐指定编码
    f.write(text)

with open("output.txt", 'r') as f:
    found = False
    for line_num, line in enumerate(f, 1):
        if target in line:
            highlighted = line.replace(target, f"{Fore.RED}{target}{Style.RESET_ALL}")
            print(f"{Fore.RED}{target}{Fore.WHITE}在第 {line_num} 行: {highlighted.strip()}")
            found = True
    if not found:
        print("未找到目标")  # :ml-citation{ref="3,7" data="citationList"}

