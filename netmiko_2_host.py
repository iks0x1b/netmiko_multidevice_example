import json
import os
import getpass
from netmiko import ConnectHandler
from datetime import datetime

def main():
    timeObj = datetime.now()
#    auser = getpass.getuser()
    auser = input('Username:')   
    apass = getpass.getpass()
    secret = apass
    
    vyos_commands = [
            "set terminal length 0",
            "show config",
            "show interfaces"
            ]

    pano_commands = [
            "set cli pager off",
            "show config running",
            "show arp all"
            ]

    result = {}
    with open("hosts.json") as connectionargs:
         adata = json.load(connectionargs)
         for host in adata['hosts']:
             target = {
                     'device_type': host['device_type'],
                     'ip': host['address'],
                     'host': host['hostname'],
                     'username': auser,
                     'password': apass,
                     'secret': secret
                     }
             net_connect = ConnectHandler(**target)
             if target['device_type'] == "paloalto_panos":
                 for command in pano_commands:
                     output = net_connect.send_command(command)
                     print(output)
             elif target['device_type'] == "vyos_ssh":
                 for command in vyos_commands:
                     output = net_connect.send_command(command)
                     print(output)

if __name__ == "__main__":
    main()
