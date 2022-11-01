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
VM_POWER_OPERATION = ["on", "off", "shutdown", "suspend", "pause", "unpause"]


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


def vm_power_operation(vm_id, status):
    """
    This function is used to VM power operations
    status: on, off, shutdown, suspend, pause, unpause
    """
    HEADERS['Content-Type'] = 'application/vnd.vmware.vmw.rest-v1+json'

    try:
        vm_power_status_url = f'{VMREST_URL}/{vm_id}/power'
        for stt in VM_POWER_OPERATION:
            if stt == status:
                payload = status
                response = requests.request(
                    "PUT", vm_power_status_url, headers=HEADERS, data=payload)
        return print(json.dumps(response.json(), indent=4, sort_keys=True))
    except requests.exceptions.JSONDecodeError:
        return print("VM not found or status is invalid")
    except UnboundLocalError:
        return print("Status is not found or invalid status")


def help():
    HELP = """
Pre-requisites:
    export VMREST_URL=http://localhost:8697/api/vms
    export VMREST_AUTH=<AUTH_TOKEN>

    Ex. echo -n "username:password" | base64
        export VMREST_AUTH=Basic dXNlcm5hbWU6cGFzc3dvcmQ=

Usage: python3 api.py [OPTIONS]

Options:
    --api [enable|disable]             Enable or disable the VMware Fusion API
    --get-vm-list                      Get the list of VMs
    --get-vm-info [vm_id]              Get the info of a VM
    --get-vm-power-state [vm_id]       Get the power state of a VM
    --power-status [vm_id] [status]    VM power operations
                                        status: on, off, shutdown, suspend, pause, unpause
    --help, -h                         Show this help message and exit
"""

    return print(HELP)


def main():
    """Main function"""
    try:
        if "--api" in sys.argv[1]:
            enable_fusion_api(sys.argv[2])
        if "--get-vm-list" in sys.argv[1]:
            get_vm_list()
        if "--get-vm-info" in sys.argv[1]:
            get_vm_info(sys.argv[2])
        if "--get-vm-power-state" in sys.argv[1]:
            get_vm_power_state(sys.argv[2])
        if "--power-status" in sys.argv[1]:
            vm_power_operation(sys.argv[2], sys.argv[3])
        if "--help" in sys.argv[1] or "-h" in sys.argv[1]:
            help()
    except ConnectionRefusedError:
        sys.exit("\nThe host is not responding or don't exist\n")
    except requests.exceptions.ConnectionError:
        print(sys.exit("\nError connecting to the host\n"))
    except IndexError:
        sys.exit(f"\n{help()}\n")
    except KeyboardInterrupt:
        sys.exit("\nExiting...")


if __name__ == '__main__':
    main()
