"""
Script to interact with VMware Fusion API to control VMs.
"""
# -*- coding: utf-8 -*-

import os
import json
import subprocess
import sys
import requests

VMREST_URL = os.environ.get('VMREST_URL')
VMREST_AUTH = os.environ.get('VMREST_AUTH')
PAYLOAD = {}
HEADERS = {
    'Accept': 'application/vnd.vmware.vmw.rest-v1+json',
    'Authorization': VMREST_AUTH
}


def enable_fusion_api(function):
    """This function is used to enable or disable the Fusion API"""
    try:
        if VMREST_URL:
            if function == "enable":
                try:
                    cmd_ena_api = "nohup vmrest > /tmp/vmrest.out 2>&1 &"
                    subprocess.call(cmd_ena_api, shell=True)
                    msg = "VMware Fusion API enabled"
                except ValueError:
                    msg = "VMware Fusion API already enabled"

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
        else:
            msg = "VMREST_URL not set, please set it in the environment variable: \
                   \nEx. export VMREST_URL=http://127.0.0.1:8697/api/vms"
    except ValueError:
        msg = "VMware Fusion API is not enabled"

    return print(msg)


def get_vm_list():
    """This function is used to get the list of VMs"""
    response = requests.request(
        "GET", VMREST_URL, headers=HEADERS, data=PAYLOAD)
    return print(json.dumps(response.json(), indent=4, sort_keys=True))


def get_vm_info(vm_id):
    """ This function is used to get the info of a VM """
    try:
        vm_info_url = f'{VMREST_URL}/{vm_id}'
        response = requests.request(
            "GET", vm_info_url, headers=HEADERS, data=PAYLOAD)
        return print(json.dumps(response.json(), indent=4, sort_keys=True))
    except requests.exceptions.JSONDecodeError:
        return print("VM not found or url is invalid")


def get_vm_power_state(vm_id):
    """This function is used to get the power state of a VM"""
    try:
        vm_power_state = f'{VMREST_URL}/{vm_id}/power'
        response = requests.request(
            "GET", vm_power_state, headers=HEADERS, data=PAYLOAD)
        return print(json.dumps(response.json(), indent=4, sort_keys=True))
    except requests.exceptions.JSONDecodeError:
        return print("VM not found or url is invalid")


if __name__ == '__main__':
    try:
        if "--api" in sys.argv[1]:
            enable_fusion_api(sys.argv[2])
        if "--get-vm-list" in sys.argv[1]:
            get_vm_list()
        if "--get-vm-info" in sys.argv[1]:
            get_vm_info(sys.argv[2])
        if "--get-vm-power-state" in sys.argv[1]:
            get_vm_power_state(sys.argv[2])
    except ConnectionRefusedError:
        sys.exit("\nThe host is not responding or don't exist\n")
    except requests.exceptions.ConnectionError:
        print(sys.exit("\nError connecting to the host\n"))
    except IndexError:
        sys.exit("\nPlease, check the arguments\n")
    except KeyboardInterrupt:
        sys.exit("\nExiting...")
