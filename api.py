"""
Script to interact with VMware Fusion API to control VMs.
"""
# -*- coding: utf-8 -*-

import json
import subprocess
import sys
import requests

URL = "http://localhost:8697/api/vms"
BASIC_AUTH = 'Basic ZmxvcmVudGlubzpGPWU1YWNkMTgwOA=='
PAYLOAD = {}
HEADERS = {
    'Accept': 'application/vnd.vmware.vmw.rest-v1+json',
    'Authorization': BASIC_AUTH
}


def enable_fusion_api(function):
    """This function is used to enable or disable the Fusion API"""
    if function == "enable":
        cmd_ena_api = "nohup vmrest > /tmp/vmrest.out 2>&1 &"
        subprocess.call(cmd_ena_api, shell=True)
        msg = "VMware Fusion API enabled"

    if function == "disable":
        try:
            cmd_get_pid = "ps aux |grep vmrest |grep -v grep |awk '{ print $2 }'"
            with subprocess.Popen(cmd_get_pid, shell=True, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT) as proc:
                result = int(proc.communicate()[0].decode('utf-8'))
                cmd_kill_pid = "kill -9 " + str(result)
            with subprocess.Popen(cmd_kill_pid, shell=True,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT) as process:
                process.wait()
                msg = "VMware Fusion API disabled"
        except ValueError:
            msg = "VMware Fusion API already disabled"

    return print(msg)


def get_vm_list():
    """This function is used to get the list of VMs"""
    try:
        response = requests.request("GET", URL, headers=HEADERS, data=PAYLOAD)
        return print(json.dumps(response.json(), indent=4, sort_keys=True))
    except requests.exceptions.RequestException:
        return print("VMware Fusion API is not enabled")


def get_vm_info(vm_id):
    """ This function is used to get the info of a VM """
    response = requests.request(
        "GET", URL + "/" + vm_id, headers=HEADERS, data=PAYLOAD)
    return response.json()


def get_vm_power_state(vm_id):
    """This function is used to get the power state of a VM"""
    response = requests.request(
        "GET", URL + "/" + vm_id + "/power", headers=HEADERS, data=PAYLOAD)
    return response.json()


if __name__ == '__main__':
    try:
        if "--api" in sys.argv[1]:
            enable_fusion_api(sys.argv[2])
        if "--get-vm-list" in sys.argv[1]:
            get_vm_list()
        else:
            print("Usage: vmware_fusion.py --api [enable|disable]")
            print("Usage: vmware_fusion.py --get-vm-list")
    except ConnectionRefusedError:
        sys.exit("\nThe host is not responding or don't exist\n")
    except requests.exceptions.ConnectionError:
        print(sys.exit("\nError connecting to the host\n"))
    except IndexError:
        sys.exit("\nPlease, check the arguments\n")
    except KeyboardInterrupt:
        sys.exit("\nExiting...")
